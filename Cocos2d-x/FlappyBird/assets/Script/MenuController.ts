const {ccclass, property} = cc._decorator;

@ccclass
export default class MenuController extends cc.Component {

    GameStart(){
        /**
         * Todo 1:
         * 1. Use cc.director.loadScene() to change current scene to "game"
         */
		 cc.director.loadScene("game");
    }
}
