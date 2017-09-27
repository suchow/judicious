"""Imprudent."""

import os

from flask import Flask

app = Flask(__name__)


@app.route('/')
def hello_world():
    """Sample route."""
    return 'Hello, World!'


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, use_reloader=True)
