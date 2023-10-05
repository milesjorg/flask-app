const matterContainer = document.querySelector("#matter-container");

var Engine = Matter.Engine,
    Render = Matter.Render,
    Runner = Matter.Runner,
    Composite = Matter.Composite,
    Composites = Matter.Composites,
    Common = Matter.Common,
    MouseConstraint = Matter.MouseConstraint,
    Mouse = Matter.Mouse,
    Bodies = Matter.Bodies;

// create engine
var engine = Engine.create();
// create renderer
var render = Render.create({
  element: matterContainer,
  engine: engine,
  options: {
    width: matterContainer.clientWidth,
    height: matterContainer.clientHeight,
    wireframes: false,
    background: "transparent"
  }
});



// add bodies
var stack = Composites.stack(20, 20, 20, 5, 0, 0, function(x, y) {
    return Bodies.circle(x, y, Common.random(10, 20), { friction: 0.00001, restitution: 0.5, density: 0.001 });
});

Composite.add(engine.world, stack);

Composite.add(engine.world, [
    Bodies.rectangle(200, 150, 700, 20, { isStatic: true, angle: Math.PI * 0.06, render: { fillStyle: '#060a19' } }),
    Bodies.rectangle(500, 350, 700, 20, { isStatic: true, angle: -Math.PI * 0.06, render: { fillStyle: '#060a19' } }),
    Bodies.rectangle(340, 580, 700, 20, { isStatic: true, angle: Math.PI * 0.04, render: { fillStyle: '#060a19' } })
]);

// add mouse control
var mouse = Mouse.create(render.canvas),
mouseConstraint = MouseConstraint.create(engine, {
    mouse: mouse,
    constraint: {
        stiffness: 0.2,
        render: {
            visible: false
        }
    }
});

Composite.add(engine.world, mouseConstraint);

// keep the mouse in sync with rendering
render.mouse = mouse;

// fit the render viewport to the scene
// Render.lookAt(render, Composite.allBodies(engine.world));

// wrapping using matter-wrap plugin
for (var i = 0; i < stack.bodies.length; i += 1) {
    stack.bodies[i].plugin.wrap = {
        min: { x: render.bounds.min.x, y: render.bounds.min.y },
        max: { x: render.bounds.max.x, y: render.bounds.max.y }
    };
}

Render.run(render);
const runner = Runner.create();
Runner.run(runner, engine);

function handleResize(matterContainer) {
    render.canvas.width = matterContainer.clientWidth;
    render.canvas.height = matterContainer.clientHeight;
    
    // reposition ground
    // Matter.Body.setPosition(ground, Matter.Vector.create(
        //     matterContainer.clientWidth / 2,
        //     matterContainer.clientHeight
        // ));
    }

window.addEventListener("resize", () => handleResize(matterContainer));