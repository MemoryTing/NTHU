import GameController from "./GameController";

const {ccclass, property} = cc._decorator;

@ccclass
export default class PipeController extends cc.Component {

    player: cc.Node = null;

    Canvas:cc.Node = null;

    isPass:boolean = false;
    onLoad()
    {
        this.Canvas = cc.find("Canvas");
        this.player = cc.find("Canvas/Player");
    }

    update (dt) {

        if(this.node.x < this.player.x && this.isPass == false){
            this.Canvas.getComponent(GameController).AddScore();
            this.isPass = true;
        }

        if(this.node.x < -500){
            this.node.destroy();
        }else{
            this.node.x -= dt * 200;
        }
    }
}
