var Example = Example || {};

Example.mixed = function() {
    var Engine = Matter.Engine,
        Render = Matter.Render,
        Runner = Matter.Runner,
        Composites = Matter.Composites,
        Common = Matter.Common,
        MouseConstraint = Matter.MouseConstraint,
        Mouse = Matter.Mouse,
        World = Matter.World,
        Serializer = Matter.Serializer,
        Bodies = Matter.Bodies;

    // create engine
    var engine = Engine.create(),
        world = engine.world;

    engine.world.gravity.y = 2.00;

    // create renderer
    var render = Render.create({
        element: document.getElementById("stage"),
        engine: engine,
        options: {
            width: 600,
            height: 400,
            // showAngleIndicator: true,
            // width: 800,
            // height: 600,
            // pixelRatio: 2,
            background: '#ffffff',
            wireframeBackground: '#222',
            // hasBounds: false,
            // enabled: true,
            wireframes: false,
            // showSleeping: true,
            // showDebug: false,
            // showBroadphase: false,
            // showBounds: false,
            // showVelocity: false,
            // showCollisions: false,
            // showSeparations: false,
            // showAxes: false,
            // showPositions: false,
            // showAngleIndicator: false,
            // showIds: false,
            // showShadows: false,
            // showVertexNumbers: false,
            // showConvexHulls: false,
            // showInternalEdges: false,
            // showMousePosition: false
        }
    });

    Render.run(render);

    // create runner
    var runner = Runner.create();
    Runner.run(runner, engine);

    var friction = 1.00;

    // add bodies
    var stack = Composites.stack(0, 300, 2, 5, 0, 0, function(x, y) {
        var sides = 4;
        var chamfer = null;
        switch (Math.round(Common.random(0, 1))) {
        case 0:
            if (Common.random() < 0.50) {
                return Bodies.rectangle(
                  x, y,
                  Common.random(25, 50), Common.random(25, 50), { chamfer: chamfer, friction: friction }
                );
            } else {
                return Bodies.rectangle(x, y, Common.random(80, 120), Common.random(25, 30), { chamfer: chamfer, friction: friction });
            }
        case 1:
            return Bodies.polygon(x, y, sides, Common.random(25, 50), { chamfer: chamfer, friction: friction });
        }
    });

    World.add(world, stack);

    World.add(world, [
        // walls
        Bodies.rectangle(400, 0, 800, 50, { isStatic: true, render: {fillStyle: "#eeeeee"} }),
        Bodies.rectangle(400, 600, 800, 50, { isStatic: true, chamfer: null, friction: friction, render: {fillStyle: "#eeeeee"} }),
        Bodies.rectangle(800, 300, 50, 600, { isStatic: true,  render: {fillStyle: "#eeeeee"}  }),
        Bodies.rectangle(0, 300, 50, 600, { isStatic: true,  render: {fillStyle: "#eeeeee"}  })
    ]);

    // add mouse control
    var mouse = Mouse.create(render.canvas),
        mouseConstraint = MouseConstraint.create(engine, {
            mouse: mouse,
            constraint: {
                stiffness: 0.8,
                render: {
                    visible: false
                }
            }
        });

    World.add(world, mouseConstraint);

    // keep the mouse in sync with rendering
    render.mouse = mouse;

    // fit the render viewport to the scene
    Render.lookAt(render, {
        min: { x: 0, y: 0 },
        max: { x: 800, y: 600 }
    });

    // context for MatterTools.Demo
    return {
        engine: engine,
        runner: runner,
        render: render,
        canvas: render.canvas,
        stop: function() {
            Matter.Render.stop(render);
            Matter.Runner.stop(runner);
        }
    };
};
