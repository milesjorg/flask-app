class Sling {
    constructor(anchor, projectile) {
        const options = {
            pointA: anchor,
            bodyB: projectile,
            stiffness: 0.01,
            length: 1,
            damping: 0.01,
            label: "sling"
        };
        this.sling = Constraint.create(options);
        World.add(engine.world, this.sling);
    };

    detach() {
        this.sling.bodyB = Bodies.circle(this.sling.pointA.x, this.sling.pointA.y, 20, {
            restitution: 1,
            frictionAir: 0.01
        });
        World.add(engine.world, this.sling.bodyB);
        firing = false;
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