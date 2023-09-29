const Engine = Matter.Engine,
  Render = Matter.Render,
  World = Matter.Composite,
  Body = Matter.Body,
  Composites = Matter.Composites,
  Bodies = Matter.Bodies,
  Bounds = Matter.Bounds,
  Runner = Matter.Runner;

const engine = Engine.create();
const runner = Runner.create();
const render = Render.create({
  element: document.getElementById("gameCanvas"),
  engine: engine,
  options: {
    width: 1200,
    height: 1000,
    wireframes: false,
    background: "grey",
    hasBounds: true,
  }
});

const bird = Bodies.circle(render.options.width / 3, render.options.height / 3, 15, {frictionAir: 0, label: "bird"});
const ground = Bodies.rectangle(0, render.options.height + 50, 100000000000, 200, {isStatic: true});

World.add(engine.world, [bird, ground]);
Body.setVelocity(bird, {x: 3, y: 0});

function spawnPipe() {
  const pipe = Bodies.rectangle(1000, 250, 50, 500, {isStatic: true});
  World.add(engine.world, [pipe]);
}

let spacePressed = false;
function jump() {
  if (!spacePressed) {
    Body.applyForce(bird, bird.position, {x: 0, y: -0.04});
    console.log("space pressed")
    spacePressed = true;
  }
}

document.addEventListener("keydown", function(event) {
  if (event.code === "Space") {
    jump();
  };
});

document.addEventListener("keyup", function(event) {
  if (event.code === "Space") {
    spacePressed = false;
  };
});

Runner.run(engine);
Render.run(render);
// let translate = {x: 3, y: 0};
// Bounds.translate(render.bounds, translate);

function followPlayer() {
  const canvas = render.canvas;
  const ctx = canvas.getContext('2d');

  const playerX = bird.position.x;
  const playerY = bird.position.y;

  const canvasCenterX = bird.position.x / 2;
  const canvasCenterY = bird.position.y / 2;
  
  const cameraX = playerX - canvasCenterX;
  const cameraY = playerY - canvasCenterY;

  ctx.translate(-cameraX, -cameraY);
}

function gameLoop() {
  followPlayer();
  requestAnimationFrame(gameLoop);
}

gameLoop();