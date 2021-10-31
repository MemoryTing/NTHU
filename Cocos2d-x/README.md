## FlappyBird
### Goal
通過鍵盤或滑鼠控制鳥的跳躍，跳過水管即可得分，若撞擊在水管或是地面上則遊戲結束。
### Details
The steps to finish the FlappyBird template.
1. Change Scene
    Change scene from menu to game.
2. Generate Pipes 
    Use pipe prefab to generate pipe in GameController.
3. Score
    Update score in GameController and change the     string of RichText with current score information.
4. Show restart button
    When the player is dead, let the restart button be active.
5. Register Event
    Enable keyboard input and call assigned function, then we can control the player by both keyboard and mouse. (Given template already finished the mouse part.)
6. Connect node to script
### Result
<img src="https://i.imgur.com/yxwhttt.gif" width=50%>

***
## Rockman
### Goal
使用鍵盤的'Z'和'X'控制Rockman的移動
使用鍵盤的'j'進行射擊，若擊中敵軍即可得分
使用鍵盤的'k'進行跳躍，可躲避敵軍或跳至木箱上
### Details
The steps to finish the Rockman template.
1. Set Box’s Physical Property
    Make the block fix on the ground, and it won’t move when player collide with it.
3. Create Jump Animation
    Create a new animation clip named 'jump', and mount all the animation clips of player. ( Others animation clip are given, there are 'move', 'shoot', 'idle' and 'reborn')
5. Set Reborn Effect
    When the player die, reset the player's position to the position it generates.
    And restart.
7. Set Jump Effect
    Set rigid body’s linear velocity to create jump effect.
9. Check Collision
    Use otherCollider.tag to check if the player collides with ground or block. If the condition is true, set the value of this.onGround to true and check if jump animation still playing, if yes, stop it and play idle animation.
### Result
<img src="https://i.imgur.com/j7CAyPJ.gif" width=50%>

