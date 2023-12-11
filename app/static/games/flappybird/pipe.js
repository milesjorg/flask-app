class Pipe {
    constructor(posX) {
        [this.topPipeHeight, this.bottomPipeHeight] = generatePipeHeights();
        this.topPipe = Bodies.rectangle(posX, this.topPipeHeight / 2, pipeWidth, this.topPipeHeight, { isStatic: true, label: "pipe" });
        this.bottomPipe = Bodies.rectangle(posX, render.options.height - (this.bottomPipeHeight / 2), pipeWidth, this.bottomPipeHeight, { isStatic: true, label: "pipe" });
        World.add(engine.world, [this.topPipe, this.bottomPipe]);
    };
}