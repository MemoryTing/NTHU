const {ccclass, property} = cc._decorator;

@ccclass
export default class score extends cc.Component 
{
    private value: number = 0;

    onLoad () 
    {
        this.resetScore();
    }

    public resetScore()
    {
        this.value = 0;

        this.node.getComponent(cc.Label).string = "Score: 0";
    }

    public addOnePoint()
    {
        this.value++;

        this.node.getComponent(cc.Label).string = "Score: " + this.value.toString();
    }
}
