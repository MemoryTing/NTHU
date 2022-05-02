# NTHU
#### 將在學期間做過比較完整的作業及專題進行整理，根據作品內容進行分類，每個資料夾內包含各自的readme.md介紹各個作業內容

* Battle Game

  使用C library Allegro 5製作簡易的雙人對戰遊戲

* Comments Analysis

  分析台灣粉絲數排名靠前的YouTuber在YouTube影片底下所獲得的留言，並和PTT上討論該YouTuber的留言進行比較

* Computer Graphics

  使用OpenGL對給定的模型進行翻轉伸縮、光線調整及材質改變等等變化

* Key Finding Algorithms

  使用Python Package librosa對歌曲進行分析，找出該歌曲片段的調性，並計算不同曲風的準確度

* Mango Image Recognition

  將dataset中已標記的芒果圖片作為分級標準，並使用train好的model對未知等級的芒果圖片進行分級標記

## Baby Monitor
#### Goal
偵測睡眠中的嬰兒的生命徵象數值，在離開嬰兒身邊時也能確定他的狀態，若無法偵測到心跳呼吸，則立即傳送通知。
#### Device
使用mmWave EVM Kit毫米波感測模組與Raspberry Pi3抓取感測器正前方範圍30至90公分的微小震動數據，取得數據後，輔以開發商提供之mmWave Python Library進行數據分析，將心跳及呼吸的數據分別濾出。

#### Result
抓取數據建立dataset，並使用sklearn中的函式進行迴歸分析，並將結果用於判斷目前即時獲得的心跳呼吸資訊屬於何種狀態

> alert　前方沒有人或前方的人心跳呼吸過慢甚至停止
> human　前方有人，且心跳呼吸正常
> move　前方有人，且正在移動

即時將偵測結果上傳firebase，並由網站的形式進行結果的呈現

#### URL　https://github.com/LYW0288/baby_monitor



## 3D Crazy Arcade

#### Goal

使用網頁建立3D版的爆爆王

#### Rules

進到準備畫面後，共有兩張地圖可自由選擇進入。遊戲將以第一人稱視角的方式進行，玩家可使用方向鍵進行前後左右的移動，而滑鼠的移動可使視角旋轉。

玩家可任意放置水球，水球將在5秒後爆炸，若是放下後未即時遠離將會導致遊戲結束；場上會有技能方塊，獲得技能方塊將能隨機獲得一個技能：

1. 多一顆水球：

   遊戲設定一次只能放置一顆水球，當水球爆炸後才能放置第二顆，因此此技能可讓使用者在已放置一顆水球的情況下再放置一顆至其他位置。此技能限用一次。

2. 跳躍：

   獲得跳躍技能後，可在5秒內跳高觀察地圖，幫助玩家決定前進方向

除玩家外將會有六名NPC隨機出現在地圖中，唯有找到對手並讓他被水球炸到方可勝利

#### URL　https://github.com/LYW0288/bombombking

