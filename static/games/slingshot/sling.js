class Sling {
    constructor(anchor, body) {
        const options = {
            pointA: anchor,
            bodyB: body,
            stiffness: 0.01,
            length: 1,
            damping: 0.01,
            label: "sling"
        };
        this.sling = Constraint.create(options);
        World.add(engine.world, this.sling);
    };

    detach() {
        World.remove(engine.world, this.sling);
    }
    
    reset(anchor, body) {
        this.detach()
        Body.setSpeed(body, 0);
        Body.setPosition(body, anchor);
        this.sling.pointA = anchor;
        this.sling.bodyB = body;
        World.add(engine.world, this.sling)
    }

}