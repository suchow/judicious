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

    var friction = 2.00;

    // // add bodies
    // var stack = Composites.stack(0, 300, 2, 5, 0, 0, function(x, y) {
    //     var sides = 4;
    //     var chamfer = null;
    //     switch (Math.round(Common.random(0, 1))) {
    //     case 0:
    //       return Bodies.rectangle(x, y, 100, 25, { chamfer: chamfer, friction: friction });
    //     case 1:
    //     return Bodies.rectangle(x, y, 45, 45, { chamfer: chamfer, friction: friction });
    //     }
    // });
    chamfer = null;
    x = 600;
    y = 400;
    options = { chamfer: chamfer, friction: friction };
    World.add(world, [
      Bodies.rectangle(Common.random(0, x), Common.random(0, y), 200, 50, options),
      Bodies.rectangle(Common.random(0, x), Common.random(0, y), 100, 100, options),
      Bodies.rectangle(Common.random(0, x), Common.random(0, y), 50, 50, options),
      Bodies.rectangle(Common.random(0, x), Common.random(0, y), 50, 100, options),
      Bodies.rectangle(Common.random(0, x), Common.random(0, y), 100, 50, options),
      Bodies.rectangle(Common.random(0, x), Common.random(0, y), 200, 50, options),
      Bodies.rectangle(Common.random(0, x), Common.random(0, y), 200, 50, options),
      Bodies.rectangle(Common.random(0, x), Common.random(0, y), 200, 50, options),
    ]);

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
                stiffness: 1.0,
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
