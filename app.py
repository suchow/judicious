"""Imprudent."""

from datetime import datetime, timedelta
from functools import wraps
import json
import os
import random
import uuid


from flask import (
    abort,
    Flask,
    g,
    jsonify,
    redirect,
    render_template,
    request,
    session,
    url_for,
)
from flask_sockets import Sockets
from flask_sqlalchemy import SQLAlchemy
import gevent
from pq import PQ
from psycopg2 import connect
from raven.contrib.flask import Sentry
import redis
import requests
from sqlalchemy.dialects.postgresql import UUID

app = Flask(__name__)

sockets = Sockets(app)

REDIS_URL = os.environ['REDIS_URL']
REDIS_CHAN = 'chat'
REDIS_TLS_URL = os.environ.get('REDIS_TLS_URL', REDIS_URL)
redis = redis.from_url(REDIS_TLS_URL, ssl_cert_reqs=None)

app.secret_key = os.environ["JUDICIOUS_SECRET_KEY"]

DB_URL_DEFAULT = 'postgresql://postgres@localhost/judicious'
DB_URL = os.environ.get("DATABASE_URL", DB_URL_DEFAULT)

if DB_URL.startswith("postgres://"):
    DB_URL = DB_URL.replace("postgres://", "postgresql://", 1)
    
app.config['SQLALCHEMY_DATABASE_URI'] = DB_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JUDICIOUS_LOG_LEVEL'] = os.environ["JUDICIOUS_LOG_LEVEL"]
db = SQLAlchemy(app)

sentry = Sentry(app)

# Create the queues.
conn = connect(DB_URL)
pq = PQ(conn)


class Task(db.Model):
    """A task to be completed by a judicious participant."""

    __tablename__ = "task"

    id = db.Column(UUID, primary_key=True, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now)
    last_queued_at = db.Column(db.DateTime)
    type = db.Column(db.String(64), nullable=False)
    parameters = db.Column(db.JSON)
    person_id = db.Column(UUID, db.ForeignKey('person.id'))
    context_id = db.Column(UUID, db.ForeignKey('context.id'), nullable=False)
    last_started_at = db.Column(db.DateTime)
    finished_at = db.Column(db.DateTime)
    result = db.Column(db.JSON)

    def __init__(self, id, context_id, type, parameters=None):
        self.id = id
        self.context_id = context_id
        self.type = type
        self.parameters = parameters

    def __repr__(self):
        return '<Task %r>' % self.type

    def timeout(self):
        """Placed timed-out tasks back on the queue."""
        app.logger.info("Timeout on task {}, requeuing.".format(self.id))
        self.last_started_at = None
        self.last_queued_at = datetime.now()
        db.session.add(self)
        db.session.commit()
        self.requeue()

    def requeue(self):
        task_id = str(self.id)  # Convert UUID to string
        if self.person_id:
            person_id = str(self.person_id)  # Convert UUID to string
            pq[person_id].put({"id": task_id})
        else:
            pq["open"].put({"id": task_id})


class Person(db.Model):
    """An identity to be claimed by a judicious participant."""

    __tablename__ = "person"

    id = db.Column(UUID, primary_key=True, nullable=False)
    context_id = db.Column(UUID, db.ForeignKey('context.id'))
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now)
    claimed_at = db.Column(db.DateTime)
    tasks = db.relationship("Task", backref='person')

    def __init__(self, id, context_id):
        self.id = id
        self.context_id = context_id

    def __repr__(self):
        return '<Person %r>' % self.id


class Context(db.Model):
    """A particular run of a script."""

    def __init__(self, id):
        self.id = id

    def __repr__(self):
        return '<Context %r>' % self.id

    id = db.Column(UUID, primary_key=True, nullable=False)
    tasks = db.relationship("Task", backref='context')
    persons = db.relationship("Person", backref='context')


@app.context_processor
def inject_sentry_dsn():
    return dict(SENTRY_DSN_FRONTEND=os.environ.get("SENTRY_DSN_FRONTEND"))


@app.errorhandler(500)
def internal_server_error(error):
    return render_template(
        '500.html',
        event_id=g.sentry_event_id,
        public_dsn=sentry.client.get_public_dsn('https')
    ), 500


@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404


def require_api_key(view_function):
    @wraps(view_function)
    def decorated_function(*args, **kwargs):
        if request.args.get("key") == os.environ["JUDICIOUS_SECRET_KEY"]:
            return view_function(*args, **kwargs)
        else:
            abort(401)
    return decorated_function


@app.before_request
def make_session_permanent():
    session.permanent = True


@app.route('/ad/')
def ad():
    """Index route."""
    assignmentId = request.values.get("assignmentId", None)
    if assignmentId == "ASSIGNMENT_ID_NOT_AVAILABLE":
        return render_template('ad_mturk.html')
    elif assignmentId:
        return redirect(url_for('consent', _scheme='https', _external=True, **request.args))
    else:
        return render_template('index.html')


@app.route('/consent/', methods=['GET'])
def consent():
    """Render the consent form."""
    if session.get('JUDICIOUS_CONSENTED', False) is True:
        return redirect(
            url_for(
                'stage',
                _scheme='https',
                _external=True,
                **request.args))
    else:
        return render_template('consent.html')


@app.route('/assent/', methods=['GET'])
def assent():
    """Assent to participanting in the experiment."""
    session['JUDICIOUS_CONSENTED'] = True
    return redirect(url_for('stage', _scheme='https', _external=True, **request.args))


@app.route('/contexts/<context_id>', methods=['PUT'])
def put_context(context_id):
    """Add a new context."""
    if not Context.query.filter_by(id=context_id).one_or_none():
        context = Context(context_id)
        db.session.add(context)
        db.session.commit()
        return jsonify(
            status="success",
            message="Context created.",
            data={
                "id": context_id,
            }
        ), 200
    else:
        app.logger.info("Context with id {} already exists".format(context_id))
        return jsonify(
            status="success",
            message="Already exists.",
            data={
                "id": context_id,
            }
        ), 409


@app.route('/persons/<person_id>', methods=['POST'])
def post_person(person_id):
    """Add a new person."""
    person = Person(person_id)
    db.session.add(person)
    db.session.commit()


@app.route('/persons/<person_id>', methods=['GET'])
def get_person(person_id):
    """Get a person."""
    person = Person.query.filter_by(id=person_id).one_or_none()
    if person:
        return jsonify(
            status="success",
            message="Person retrieved",
            data={
                "id": person.id,
                "context_id": person.context_id,
                "created_at": person.created_at,
                "claimed_at": person.claimed_at,
                "now": datetime.now(),
            }
        ), 200
    else:
        return jsonify(
            status="success",
            message="No person with id {} found.".format(person_id),
            data={
                "id": person_id,
            }
        ), 404


@app.route('/tasks', methods=['POST'], defaults={'id': str(uuid.uuid4())})
@app.route('/tasks/<uuid:id>', methods=['POST'])
def post_task(id):
    """Add a new task to the queue.

    TODO: Respect distinction between POST and PUT.
    """
    id_string = str(id)
    if not Task.query.filter_by(id=id_string).one_or_none():

        # Create the task.
        app.logger.info("Creating task with id {}".format(id_string))
        task = Task(
            id_string,
            request.values["context"],
            request.values["type"],
            json.loads(request.values["parameters"]),
        )
        task.last_queued_at = datetime.now()

        # Check the person.
        person_id = request.values.get("person")
        if person_id and not Person.query.filter_by(id=person_id).one_or_none():
            person = Person(person_id, request.values["context"])
            db.session.add(person)
            db.session.commit()

        task.person_id = person_id
        db.session.add(task)
        db.session.commit()

        # Put it on the appropriate queue.
        if person_id:
            queue_name = person_id.replace("-", "_")
            redundancy = 1
        else:
            queue_name = "open"
            redundancy = int(os.environ.get("JUDICIOUS_REDUNDANCY", 1))

        for i in range(redundancy):
            if int(request.values.get("priority")) > 0:
                expected_at = timedelta(seconds=i*20)
            else:
                expected_at = timedelta(days=random.randint(1, 365*10))

            pq[queue_name].put({"id": id_string}, expected_at=expected_at)

        return jsonify(
            status="success",
            message="Task posted.",
            data={
                "id": id_string,
            }
        ), 200

    else:
        app.logger.info("Task with id {} already exists".format(id))
        return jsonify(
            status="success",
            message="Already exists.",
            data={
                "id": id_string,
                "type": type,
            }
        ), 409


@app.route('/tasks/<uuid:id>', methods=['PATCH'])
def patch_task(id):
    """Add a result to the given task."""
    result = request.values["result"]
    id_string = str(id)
    task = Task.query.filter_by(id=id_string).one()
    if task.result:
        return jsonify(
            status="error",
            message="A result has already been added.",
            data={
                "id": id,
            }
        ), 409
    else:
        task.result = json.loads(result)
        task.finished_at = datetime.now()
        db.session.add(task)
        db.session.commit()
        return jsonify(
            status="success",
            message="Result added.",
            data={
                "id": id,
            }
        ), 200


@app.route('/tasks/<uuid:id>', methods=['GET'])
def get_task_result(id):
    """Get the result of a task."""
    task = Task.query.filter_by(id=str(id)).one_or_none()
    if not task:
        return jsonify(
            status="success",
            message="No task with id {} found.".format(id),
            data={
                "id": id,
            }
        ), 404
    elif not task.result:
        return jsonify(
            status="success",
            message="Task is not yet complete.",
            data={
                "id": id,
            }
        ), 202
    else:
        return jsonify(
            status="success",
            message="Task complete.",
            data={
                "id": task.id,
                "type": task.type,
                "result": task.result,
                "created_at": task.created_at,
                "last_started_at": task.last_started_at,
                "last_queued_at": task.last_queued_at,
                "finished_at": task.finished_at,
            }
        ), 200


@app.route('/stage/', methods=['GET'])
def stage():
    """Serve the next task."""
    if session.get('PERSONS'):
        persons = Person.query.filter(Person.id.in_(session['PERSONS'])).all()
    else:
        persons = []

    app.logger.info("Persons in session are {}".format(persons))

    task_id = None
    if not task_id:
        app.logger.info("Looking for tasks assigned to existing persons...")
        for person in persons:
            queue = pq[person.id.replace("-", "_")]
            if len(queue):
                task_id = queue.get()
                break

    contexts = [person.context for person in persons]
    app.logger.info(contexts)
    if not task_id:
        app.logger.info("Looking for unclaimed persons.")
        if persons:
            person = (
                Person.query
                .filter(~Person.context_id.in_(c.id for c in contexts))
                .filter(Person.claimed_at == None)  # noqa
                .order_by(Person.created_at.asc())
                .limit(1).one_or_none()
            )
        else:
            person = (
                Person.query
                .filter(Person.claimed_at == None)  # noqa
                .order_by(Person.created_at.asc())
                .limit(1).one_or_none()
            )

        if person:
            app.logger.info("Person {} has been claimed.".format(person.id))
            person.claimed_at = datetime.now()
            db.session.add(person)
            db.session.commit()
            task_id = pq[person.id.replace("-", "_")].get()
            persons.append(person)
            session["PERSONS"] = [p.id for p in persons]

    if not task_id:
        app.logger.info("Popping a task off the open queue.")
        open_queue = pq["open"]
        if len(open_queue):
            task_id = open_queue.get()

    if not task_id:
        app.logger.info("No tasks are available.")
        return render_template("no_tasks.html")

    task = Task.query.filter_by(id=task_id.data['id']).one_or_none()
    task.last_started_at = datetime.now()
    db.session.add(task)
    db.session.commit()
    return render_template(
        "tasks/{}.html".format(task.type),
        task=task,
        RECAPTCHA_SITE_KEY=os.environ['RECAPTCHA_SITE_KEY']
    )


@app.route('/recaptcha/', methods=['POST'])
def recaptcha():
    """Verify the recaptcha."""
    app.logger.info(request.values["response"])
    r = requests.post(
        'https://www.google.com/recaptcha/api/siteverify',
        data={
            'secret': os.environ['RECAPTCHA_SECRET_KEY'],
            'response': request.values["response"],
        }
    )
    return jsonify(
        status="success",
        message="Recaptcha passed.",
        data={
            "solved": r.json()['success'],
        }
    ), 200


class ChatBackend(object):
    """Interface for registering and updating WebSocket clients."""

    def __init__(self):
        self.clients = list()
        self.pubsub = redis.pubsub()
        self.pubsub.subscribe(REDIS_CHAN)

    def __iter_data(self):
        for message in self.pubsub.listen():
            data = message.get('data')
            if message['type'] == 'message':
                app.logger.info(u'Sending message: {}'.format(data))
                yield json.dumps(data.decode("utf-8"))

    def register(self, client):
        """Register a WebSocket connection for Redis updates."""
        self.clients.append(client)

    def send(self, client, data):
        """Send data to the registered client. Discard invalid connections."""
        try:
            client.send(data)
        except Exception:
            self.clients.remove(client)

    def run(self):
        """Listen for new messages in Redis, and send them to clients."""
        for data in self.__iter_data():
            for client in self.clients:
                gevent.spawn(self.send, client, data)

    def start(self):
        """Maintain Redis subscription in the background."""
        gevent.spawn(self.run)


chats = ChatBackend()
chats.start()


@app.route('/')
def hello():
    return render_template('index.html')


@sockets.route('/submit')
def inbox(ws):
    """Receives incoming chat messages, inserts them into Redis."""
    while not ws.closed:
        # Sleep to prevent constant context switches.
        gevent.sleep(0.1)
        message = ws.receive()

        if message:
            app.logger.info(u'Inserting message: {}'.format(message))
            redis.publish(REDIS_CHAN, message)


@sockets.route('/receive')
def outbox(ws):
    """Sends outgoing chat messages, via `ChatBackend`."""
    chats.register(ws)

    while not ws.closed:
        # Context switch while `ChatBackend.start` runs in the background.
        gevent.sleep(0.1)


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, use_reloader=True)
