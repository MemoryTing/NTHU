import AudioController from './AudioController'
const { ccclass, property } = cc._decorator;

@ccclass
export default class GameController extends cc.Component {

    @property(cc.Prefab)
    pipe: cc.Prefab = null;

    @property(cc.Node)
    background: cc.Node = null;

    @property(cc.Node)
    restartButton: cc.Node = null;

    @property(cc.RichText)
    scoreText: cc.RichText = null;
    score = 0;

    second = 0;
    duration = 2.0;
    // Minimum pipe offset
    pipeMin = 50;
    // Maximum pipe offset
    pipeMax = 100;

    audio:cc.Node = null;

    start() {
        this.audio = cc.find("Canvas/Audio");
    }

    update(dt) {
        if (this.second > this.duration) {
            /**
             * Todo 2: 
             * 1. Use cc.instantiate() and this.pipe to generate new pipe and save it to variable "newpipe"
             * 2. Use this.setupPipe() to setup "newpipe"
             * 3. Use addChild() to let newpipe become this.background's child
             * 4. Return this.second to zero
             */

			var newpipe = cc.instantiate(this.pipe);
            this.setupPipe(newpipe);
            this.background.addChild(newpipe);
            this.second = 0;

        } else {
            this.second += dt;
        }
    }

    setupPipe(pipe) {
        pipe.x = 465;
        var prop = Math.random();
        if (prop > 0.5) {
            pipe.y += this.getRandom(this.pipeMin, this.pipeMax);
        } else {
            pipe.y -= this.getRandom(this.pipeMin, this.pipeMax);
        }
    }

    getRandom(min, max) {
        return Math.floor(Math.random() * (max - min + 1)) + min;
    }

    AddScore(){
        /**
         * Todo 3: 
         * 1. Plus one point to this.score 
         * 2. Change this.scoreText's string with BBCode format
         */
		this.score += 1;
        this.scoreText.string = this.score.toString();

        this.audio.getComponent(AudioController).playGetPointAudio();
    }


    PlayerDead() {
        /**
         * Todo 4:
         * 1. Change restartButton active to true
         */
		this.restartButton.active = true;

		this.audio.getComponent(AudioController).playDeadAudio();

		cc.game.pause();

    }

    
    RestartGame() {
        cc.game.resume();
        cc.director.loadScene("game");
    }
}
