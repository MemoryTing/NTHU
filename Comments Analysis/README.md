## Comments Analysis

### Goal

分析台灣粉絲數排名靠前的YouTuber在YouTube影片底下所獲得的留言，並和PTT上討論該YouTuber的留言進行比較

### Details

1. 爬蟲

   - 在Google Cloud Platform上使用YouTube Data API v3抓取指定YouTuber最新影片底下的所有留言
   - 選擇在 PTT 上較為熱門的四個版的內容：KoreaDrama 韓劇版、Gossiping 八卦版、Movie 電影版、C_Chat 希洽版。 每一個版爬二十篇推數超過 50 的文章，使用Python sentiment analysis tool senti_c計算正負留言占所有留言之比例

2. PTT 和 YouTube 的留言偏好比較

   個別分析單一YouTuber在PTT和YouTube上獲得的留言中正負面留言比例，並進行比較

3. 詞頻分析

   個別統計出單支影片中正面留言的高頻詞和負面留言的高頻詞，並使用WordCloud的方式呈現

4. 忠實粉絲留言分析

   將連續三部影片皆留言的粉絲標註為忠實粉絲，並統計各YouTuber的忠實粉絲數和訂閱數之間的關係

   分析定義為忠實粉絲帳號其留言內容，又可再區分為忠實粉絲、黑粉、假粉三大類