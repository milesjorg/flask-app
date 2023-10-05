const Engine = Matter.Engine,
    Render = Matter.Render,
    World = Matter.Composite,
    Events = Matter.Events,
    Composites = Matter.Composites,
    Bodies = Matter.Bodies,
    Body = Matter.Body,
    Constraint = Matter.Constraint,
    Mouse = Matter.Mouse,
    MouseConstraint = Matter.MouseConstraint,
    Runner = Matter.Runner;

const engine = Engine.create();
const runner = Runner.create();
const render = Render.create({
    element: document.getElementById("game_container"),
    engine: engine,
    options: {
        width: 1600,
        height: 1000,
        wireframes: false,
        background: "grey"
    }
});

const ground = Bodies.rectangle(render.options.width / 2, render.options.height, render.options.width, 75, { isStatic: true });
const ceiling = Bodies.rectangle(render.options.width / 2, 0, render.options.width, 75, { isStatic: true });
const wallLeft = Bodies.rectangle(0, render.options.height / 2, 75, render.options.height, { isStatic: true });
const wallRight = Bodies.rectangle(render.options.width, render.options.height / 2, 75, render.options.height, { isStatic: true });

const pyramid = Composites.pyramid(1350, 600, 8, 8, 0, 0, function (x, y) {
    return Bodies.rectangle(x, y, 20, 20);
});


// Can have its own table class
const leg1 = Bodies.rectangle(1400, 850, 40, 100, {
    friction: 1,
});
const leg2 = Bodies.rectangle(1500, 850, 40, 100, {
    friction: 1,
});
const tableTop = Bodies.rectangle(1450, 700, 350, 20, {
    friction: 1,
});


// const frontRim = Bodies.rectangle(1000, 200, 65, 15, {isStatic: true});
// const bottomRim = Bodies.rectangle(1000, 200, 65, 15, {isStatic: true});
// const backRim = Bodies.rectangle(1000, 200, 65, 15, {isStatic: true});
const frontRim = Bodies.rectangle(850, 250, 20, 100, { isStatic: true });
const backRim = Bodies.rectangle(950, 250, 20, 100, { isStatic: true });
const bottomRim = Bodies.rectangle(900, 300, 100, 20, { isStatic: true });

// Create a compound body to group the rectangles
const concaveRect = Body.create({
  parts: [frontRim, backRim, bottomRim],
  isStatic: true,
});

// Slingshot
const anchor = { x: 400, y: 700 };

// Can have its own class
let projectile = Bodies.circle(anchor.x, anchor.y, 20, {
    restitution: 1,
    frictionAir: 0.01
});

// Can have its own class
// let sling = new Sling(anchor, projectile);
let sling = Constraint.create({
    pointA: anchor,
    bodyB: projectile,
    stiffness: 0.01,
    length: 1,
    damping: 0.01,
    label: "sling"
});

// Can have its own class
const mouse = Mouse.create(render.canvas)
const mouseConstraint = MouseConstraint.create(engine, {
    mouse: mouse,
    constraint: {
        stiffness: 0.4,
        render: {
            visible: false
        }
    }
});
render.mouse = mouse;

document.addEventListener("keydown", function (event) {
    if (event.code === "Space") {
        sling.reset(anchor, projectile)
    }
    if (event.code === "Escape") {
        console.log(sling);
        console.log(anchor);
    }
});

let firing = false;
Events.on(mouseConstraint, "enddrag", function(e) {
    console.log(e.body);
    if (e.body === projectile) {
        firing = true;
    };
});

Events.on(engine, "afterUpdate", function () {
    if (firing && Math.abs(projectile.position.x - anchor.x) < 20 && Math.abs(projectile.position.y - anchor.y) < 20) {
        // sling.detach();
        projectile = Bodies.circle(anchor.x, anchor.y, 20, {
            restitution: 1,
            frictionAir: 0.01
        });
        World.add(engine.world, projectile);
        sling.bodyB = projectile;
        firing = false;
    }
});

World.add(engine.world, [ceiling, wallLeft, wallRight, ground, concaveRect, mouseConstraint, sling, projectile]);
Render.run(render);
Runner.run(engine);



