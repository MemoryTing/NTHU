import GameController from "./GameController";
const {ccclass, property} = cc._decorator;

@ccclass
export default class PlayerController extends cc.Component 
{
    Canvas:cc.Node = null;
    isDead:boolean = false;

    onLoad()
    {
        this.Canvas = cc.find("Canvas");

        cc.director.getCollisionManager().enabled = true;

        cc.director.getPhysicsManager().enabled = true;

        this.node.rotation = 0;

        /**
         * Todo 5:
         * 1. Register systemEvent, let cc.SystemEvent.EventType.KEY_DOWN to call this.onKeyDown function
         */
		 cc.systemEvent.on(cc.SystemEvent.EventType.KEY_DOWN , this.onKeyDown , this);
    }

    update(dt)
    {
        if(this.node.rotation < 90)
            this.node.rotation += dt * 100;
    }

    onKeyDown(event) 
    {
        switch(event.keyCode) 
        {
            case cc.KEY.space:
                this.birdFly();
                break;
        }
    }

    birdFly()
    {
        if(!this.isDead){
            this.node.getComponent(cc.RigidBody).linearVelocity = cc.v2(0, 800);
            this.node.rotation = -30;
        }
    }

    onBeginContact(contact, selfCollider, otherCollider) {
        if(otherCollider.tag != 1){
            this.Canvas.getComponent(GameController).PlayerDead();
            this.isDead = true;
            this.node.getComponent(cc.RigidBody).linearVelocity = cc.v2(0, 0);
            this.node.getComponent(cc.RigidBody).gravityScale = 0;
        }
    }
}
