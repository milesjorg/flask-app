var Engine = Matter.Engine,
  Render = Matter.Render,
  World = Matter.Composite,
  Bodies = Matter.Bodies,
  Runner = Matter.Runner;

var engine = Engine.create();
var runner = Runner.create();
var render = Render.create({
  element: document.getElementById("game_container"),
  engine: engine,
  options: {
    width: 800,
    height: 1000,
    wireframes: false,
    background: "grey"
  }
});

var ground = Bodies.rectangle(400, 950, 800, 100, { isStatic: true });

World.add(engine.world, [ground]);
Render.run(render)
Runner.run(engine);

var dropBall = function () {
  var ball = Bodies.circle(400, 20, 20);
  ball.restitution = 0.8;
  ball.frictionAir = 0.0001;
  return ball;
}

function getBall() {
  return World.allBodies(engine.world).filter(body => body.label === "Circle Body")[0];
}

function getBallPos(ball) {
  ball = getBall();
  return ball.position.y;
}

function getBallSpeed(ball) {
  ball = getBall();
  return Matter.Body.getSpeed(ball);
}

function getBallVelo(ball) {
  ball = getBall();
  return Matter.Body.getVelocity(ball).y;
}

function jump(ball) {
  ball = getBall();
  console.log(getBallVelo(ball));
  Matter.Body.setSpeed(ball, getBallSpeed(ball) * 1.5);
}

document.addEventListener("keydown", function (event) {
  if (event.code === "Space") {
    jump(getBall());
  }
})

$(".add-ball").on("click", function () {
  World.add(engine.world, dropBall());
})
