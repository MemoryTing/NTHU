const {ccclass, property} = cc._decorator;

@ccclass
export default class GroundController extends cc.Component {
    update (dt) {
        if(this.node.x < -768){
            this.node.x += 768 * 2 - dt * 200;
        }else{
            this.node.x -= dt * 200;
        }
    }
}
