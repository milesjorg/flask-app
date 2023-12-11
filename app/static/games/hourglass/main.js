const Engine = Matter.Engine,
  Render = Matter.Render,
  World = Matter.Composite,
  Body = Matter.Body,
  Composites = Matter.Composites,
  Constraint = Matter.Constraint,
  Mouse = Matter.Mouse,
  MouseConstraint = Matter.MouseConstraint,
  Bodies = Matter.Bodies,
  Bounds = Matter.Bounds,
  Events = Matter.Events,
  Runner = Matter.Runner;

const engine = Engine.create();
const runner = Runner.create();
const render = Render.create({
  element: document.getElementById("gameContainer"),
  engine: engine,
  options: {
    width: 600,
    height: 1000,
    wireframes: false,
    background: "grey",
    hasBounds: true,
  }
});

const canvas = render.canvas;
const ctx = canvas.getContext('2d');
engine.timing.timeScale = 0.7;

// Add mouse interactions
const mouse = Mouse.create(render.canvas);
const mouseConstraint = MouseConstraint.create(engine, {
    mouse: mouse
});

World.add(engine.world, [
    Bodies.rectangle(50, 200, 600, 20, { isStatic: true, angle: Math.PI * 0.2, render: { fillStyle: '#060a19' }, chamfer: {radius: 10} }),
    Bodies.rectangle(550, 200, 600, 20, { isStatic: true, angle: -Math.PI * 0.2, render: { fillStyle: '#060a19' }, chamfer: {radius: 10} }),
    Bodies.rectangle(300, 900, 400, 20, { isStatic: true, render: { fillStyle: '#060a19' } }),
    Bodies.rectangle(100, 600, 20, 600, { isStatic: true, render: { fillStyle: '#060a19' } }),
    Bodies.rectangle(500, 600, 20, 600, { isStatic: true, render: { fillStyle: '#060a19' } }),
    Composites.stack(150, -600, 40, 40, 2, 2, function(x, y) {
        return Bodies.circle(x, y, 4, { friction: 0.00001, restitution: 0, density: 0.001 })
    }),
    mouse,
    mouseConstraint
]);

Runner.run(engine);
Render.run(render);