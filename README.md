# NTHU
### 將在學期間做過比較完整的作業及專題進行整理，根據作品內容進行分類，每個資料夾內包含各自的readme.md介紹各個作業內容，畢業專題當初和組員有整理放在一起，因此另外附上連結。

## Not Yet
HTML

## 畢業專題　Baby Monitor
#### Goal
偵測睡眠中的嬰兒的生命徵象數值，在離開嬰兒身邊時也能確定他的狀態，若無法偵測到心跳呼吸，則立即傳送通知。
#### Device
使用mmWave EVM Kit毫米波感測模組與Raspberry Pi3抓取感測器正前方範圍30至90公分的微小震動數據，取得數據後，輔以開發商提供之mmWave Python Library進行數據分析，將心跳及呼吸的數據分別濾出。
#### Result
使用簡單的線性函數去分類三種情況
> alert　前方沒有人或前方的人心跳呼吸過慢甚至停止
> human　前方有人，且心跳呼吸正常
> move　前方有人，且正在移動

即時將偵測結果上傳firebase，並由網站的形式進行結果的呈現

#### URL　https://github.com/LYW0288/baby_monitor
