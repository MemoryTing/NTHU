const {ccclass, property} = cc._decorator;

@ccclass
export default class AudioController extends cc.Component {

    @property([cc.AudioClip])
    audioClips: cc.AudioClip[] = [];

    @property(cc.AudioSource)
    audioSrc: cc.AudioSource = null;

    public playGetPointAudio()
    {
        this.audioSrc.clip = this.audioClips[0];
        this.audioSrc.play();
    }

    public playDeadAudio()
    {
        this.audioSrc.clip = this.audioClips[1];
        this.audioSrc.play();
    }
}
