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
        width: 800,
        height: 1000,
        wireframes: false,
        background: "grey"
    }
});

const pan = Bodies.rectangle(render.options.width / 2, render.options.height / 2, 200, 20, {
    isStatic: true,
    angle: 1 / 16,
    inertia: Infinity,
    rotationSpeed: 0.0005
});

World.add(engine.world, [pan]);

let isMouseDown = false;

function flipPan() {
    Body.setAngle(pan, pan.angle + pan.rotationSpeed);
    requestAnimationFrame(flipPan);
}


Runner.run(engine);
Render.run(render);

document.addEventListener("mousedown", (event) => {
    if (isMouseDown) {
        flipPan(pan, isMouseDown);
        window.requestAnimationFrame(flipPan);
    };
});

document.addEventListener("mouseup", () => {
    isMouseDown = false;
    console.log("heelo");
});

// document.addEventListener("mousemove", (event) => {
//     if (isMouseDown) {
//         flipPan(pan, isMouseDown);
//     };
// });