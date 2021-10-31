const {ccclass, property} = cc._decorator;

@ccclass
export default class enemyManager extends cc.Component 
{
    @property(cc.Prefab)
    private enemyPrefab: cc.Prefab = null;

    private enemyPool = null;

    onLoad()
    {
        this.enemyPool = new cc.NodePool('enemy');

        let maxEnemyNum = 3;

        for(let i: number = 0; i < maxEnemyNum; i++)
        {
            let enemy = cc.instantiate(this.enemyPrefab);

            this.enemyPool.put(enemy);
        }

        this.schedule(this.createEnemy, 0.5); //set one enemy to the scene every 0.5s .
    }

    //call this function to add new enemy to the scene.
    private createEnemy()
    {
        let enemy = null;

        if(this.enemyPool.size() > 0)
            enemy = this.enemyPool.get(this.enemyPool);

        if(enemy != null)
            enemy.getComponent('enemy').init(this.node);
    }
    
}
