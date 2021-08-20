## Ethereum
### Goal
使用request和BeautifulSoup抓取目標地址在以太坊上的交易紀錄
記錄下目標地址的相關資料後，找尋最舊的一筆轉出資料作為下一筆目標地址，並持續進行四次查找，若無轉出資料則提早結束該次查詢。
### Files
**Ethereum.py**
從input.txt中獲得目標地址，將抓取到的交易記錄在output.txt中
**input.txt**
要抓取的目標地址列表，數量不定
**output.txt**
交易紀錄中各地址的詳細資料以及交易進行的順序
### Implement
1. 使用request抓取網頁內容。
    ```
    addr = 'https://www.blockchain.com/eth/address/' + line + '?view=standard'
    r = requests.get(addr)
    ```
2. 根據觀察網頁原始碼，找到所需資料的位置，並用BeautifulSoup中的find_all和find提取資料寫入output檔案中。
    ```
    # information of now address
    now_hash = soup.find_all('div', class_ = 'sc-1enh6xt-0 kiseLw')
	for nh in now_hash:
        name = nh.find('span', class_ = 'sc-1ryi78w-0 cILyoi sc-16b9dsl-1 ZwupP sc-1n72lkw-0 ebXUGH')
        if name.string != 'Hash':
            out_fp.write(name.string)
            out_fp.write(': ')
            name = nh.find('span', class_ = 'sc-1ryi78w-0 cILyoi sc-16b9dsl-1 ZwupP u3ufsr-0 eQTRKC')
            out_fp.write(name.string)
            out_fp.write('\n')
        else:
            now_hash = nh.find('span', class_ = 'sc-1ryi78w-0 cILyoi sc-16b9dsl-1 ZwupP u3ufsr-0 eQTRKC').string
    ```
3. Data stored in output file
    ```
    Nonce: 33
    Number of Transactions: 54
    Final Balance: 0.00179703235753823 ETH
    Total Sent: 21.62401556 ETH
    Total Received: 21.64536359235753823 ETH
    Total Fees: 0.01955100 ETH
    Date: 2018-04-20 10:49
    To: 0x4f49bdebbef29a4f1a3ea1d41867ece1850cef75
    Amount: -0.00015000 ETH
    --------------------------------------------------------------------------
    Nonce: 1
    Number of Transactions: 2
    Final Balance: 0.000075196 ETH
    Total Sent: 0.00000000 ETH
    Total Received: 0.00015000 ETH
    Total Fees: 0.000074804 ETH
    Date: 2018-04-20 10:54
    To: 0xdd007278b667f6bef52fd0a4c23604aa1f96039a
    Amount: -0.00000000 ETH
    --------------------------------------------------------------------------
    Nonce: 0
    Number of Transactions: 1,663
    Final Balance: 0.00000000 ETH
    Total Sent: 0.00000000 ETH
    Total Received: 0.00000000 ETH
    Total Fees: 0.00000000 ETH
    --------------------------------------------------------------------------
    0x03f034fb47965123ea4148e3147e2cfdc5b1f7a5 -> 0x4f49bdebbef29a4f1a3ea1d41867ece1850cef75 -> 0xdd007278b667f6bef52fd0a4c23604aa1f96039a
    --------------------------------------------------------------------------
    ```
### Reflection


***
## YouTube
### Goal
使用YouTube Data API v3抓取指定YouTube頻道最新五支影片底下的留言
### Files
**youtube_crawler.py**
　逐一讀取input.txt中列出的YouTube頻道所發布的最新影片底下的留言，並將留言內容存為json檔
**input.txt**
　準備抓取的YouTuber頻道名稱以及該頻道的channel ID
**json Folder**
　影片所屬頻道名稱加編號，數字越小影片越新
　Data內容：
　“name”：留言者的帳號名稱
　“comment”：內容
　“comment_liked”：留言被按讚的次數
　“reply_comment_number”：該則留言被回覆的留言數
### Implement
1. 在google cloud platform上開啟新專案獲取YouTube Data API v3的API KEY
    ```
    YOUTUBE_API_KEY = "AIzaSyC_gLK95fiUh3vIyLodTelcxo2pGDXzlB4"
    ```
2. 將想要獲取留言的頻道逐一記錄下該頻道的channel ID，作為input file使用
    ```
    阿滴英文
    UCeo3JwE3HezUWFdVcehQk9Q
    ```
4. 取得頻道上傳影片清單的ID
    ```
    path = f'channels?part={part}&id={channel_id}'
    data = self.get_html_to_json(path)
    try:
        uploads_id = data['items'][0]['contentDetails']['relatedPlaylists']['uploads']
    except KeyError:
        uploads_id = None
    return uploads_id
    ```
5. 從影片清單中獲取影片的ID，由於需要的是最新五支影片的留言因此max_results值設定為5
    ```
    path = f'playlistItems?part={part}&playlistId={playlist_id}&maxResults={max_results}'
    data = self.get_html_to_json(path)
    if not data:
        return []
    
    video_ids = []
    for data_item in data['items']:
        video_ids.append(data_item['contentDetails']['videoId'])
    return video_ids
    ```
6. 最後透過影片ID獲取影片底下的留言
    ```
    path = f'commentThreads?part={part}&videoId={video_id}&maxResults={max_results}&pageToken={page_token}'
    data = self.get_html_to_json(path)
    if not data:
        return [], ''
    # 下一頁的數值
    next_page_token = data.get('nextPageToken', '')
    
    # 以下整理並提取需要的資料
    comments = []
    for data_item in data['items']:
        data_item = data_item['snippet']
        top_comment = data_item['topLevelComment']
    
        author_name = top_comment['snippet'].get('authorDisplayName', '')
        if not author_name:
            author_name = ''
        comments.append({
            'name': author_name,
            'comment': top_comment['snippet']['textOriginal'],
            'comment_liked': int(top_comment['snippet']['likeCount']),
            'reply_comment_number': int(data_item['totalReplyCount'])
        })
    ```
### Reflection
之前是直接觀察HTML檔案進行crawler，因此想試試有沒有其他方法便上網參考了其他人的做法，也是第一次嘗試使用google cloud，