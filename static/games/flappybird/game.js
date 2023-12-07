const Engine = Matter.Engine,
  Render = Matter.Render,
  World = Matter.Composite,
  Body = Matter.Body,
  Composites = Matter.Composites,
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

const bird = Bodies.circle(render.options.width / 4, render.options.height / 2, 15, { frictionAir: 0.04, label: "bird" });
const ground = Bodies.rectangle(render.options.width / 2, render.options.height + 50, render.options.width, 200, { isStatic: true });
const gapSize = 200;

function randomBetween(min, max) {
  return Math.floor(Math.random() * (max - min + 1) + min);
}

function generatePipeHeights() {
  let topPipeHeight = randomBetween(100, (render.options.height / 2) - 100);
  let bottomPipeHeight = render.options.height - topPipeHeight - gapSize;

  let sizes = [topPipeHeight, bottomPipeHeight];
  if (Math.random() < 0.5) {
    sizes = sizes.reverse();
  };
  return sizes;
}

const pipeWidth = 150;
let pipePosX = render.options.width - (pipeWidth / 2);

let pipePair1 = new Pipe(pipePosX);
let pipePair2 = new Pipe(pipePosX * 1.8);

World.add(engine.world, [bird, ground, pipePair1.topPipe, pipePair1.bottomPipe, pipePair2.topPipe, pipePair2.bottomPipe]);
let pipePairs = [pipePair1, pipePair2];
const translate = { x: -1, y: 0 };
let score = 0;

Events.on(engine, "afterUpdate", function () {
  for (let i = 0; i < pipePairs.length; i++) {
    if (pipePairs[i].topPipe.position.x <= -1 * (pipeWidth / 2)) {
      pipePairs[i] = new Pipe(render.options.width * 1.6 - (pipeWidth / 2));

    } else {
      Body.translate(pipePairs[i].topPipe, translate);
      Body.translate(pipePairs[i].bottomPipe, translate);
    }
  };
});

Events.on(render, "afterRender", function() {
  ctx.font = "48px PixelFont";
  ctx.fillStyle = "white";
  ctx.fillText(score, render.options.width / 2 - 24, 40);
  for (let i = 0; i < pipePairs.length; i++) {
    if (bird.position.x == pipePairs[i].topPipe.position.x) {
      score++;
    };
  }
});

Events.on(engine, "collisionStart", function() {
  const high_score = getUserHighScore("FlappyBird")
  console.log(high_score);
  const gameData = {
    game_name: "FlappyBird",
    time_start: new Date().toISOString(),
    last_score: score,
    high_score: high_score,
  };
  ctx.font = "32px PixelFont";
  ctx.fillStyle = "red";
  ctx.fillText("GAME OVER", (render.options.width / 2) - 80, render.options.height / 3);
  Engine.clear(engine);
  Render.stop(render);
  Runner.stop(runner);
  game_over();
  sendGameData(gameData);
});

let spacePressed = false;
function jump() {
  if (!spacePressed) {
    Body.applyForce(bird, bird.position, { x: 0, y: -0.05 });
    spacePressed = true;
  }
}

document.addEventListener("keydown", function (event) {
  if (event.code === "Space") {
    jump();
  };
});

document.addEventListener("keyup", function (event) {
  if (event.code === "Space") {
    spacePressed = false;
  };
});

Runner.run(engine);
Render.run(render);

function game_over() {
  const gameOverPrompt = document.createElement('div');
  gameOverPrompt.id = 'gameOverPrompt';
  gameOverPrompt.textContent = "Play again?";
  const spaceBreak = document.createElement('br');
  const playAgainButton = document.createElement('button');
  playAgainButton.textContent = "Yes!";
  playAgainButton.id = "playAgainButton";
  const quitButton = document.createElement('button');
  quitButton.textContent = "No, I quit.";
  quitButton.id = "quitButton";

  gameOverPrompt.appendChild(spaceBreak);
  gameOverPrompt.appendChild(playAgainButton);
  gameOverPrompt.appendChild(quitButton);

  const parentElement = document.getElementById("gameContainer");
  parentElement.appendChild(gameOverPrompt);

  playAgainButton.addEventListener("click", function () {
    location.reload();
  });

  quitButton.addEventListener("click", function () {
    window.location.href = "/arcade/";
  });
}

function sendGameData(gameData) {
  fetch('/store_game_data/', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(gameData),
  });
}

function getUserHighScore() {
  fetch('/get_user_high_score/')
    .then(response => {
      if (!response.ok) {
        throw new Error(`${response.status}`)
      }
      return response.json();
    });
}