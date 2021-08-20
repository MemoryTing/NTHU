import requests
import json

YOUTUBE_API_KEY = "AIzaSyC_gLK95fiUh3vIyLodTelcxo2pGDXzlB4"

def main():
    ## Open input file
    in_fp = open('input.txt', 'r')
    channel_name = in_fp.readline()
    channel_name = channel_name.strip('\n')
    while channel_name:
        line = in_fp.readline()
        line = line.strip('\n')
        youtube_channel_id = line
        count = 1

        youtube_spider = YoutubeSpider(YOUTUBE_API_KEY)
        uploads_id = youtube_spider.get_channel_uploads_id(youtube_channel_id)
        print(uploads_id)

        video_ids = youtube_spider.get_playlist(uploads_id, max_results=5)
        print(video_ids)

        for video_id in video_ids:
            print("----------------------")
            ## Open output file
            out_name = channel_name + '_' + str(count) + '.json'
            out_fp = open(out_name, 'w', encoding='utf-8')
            print('open output file')

            next_page_token = ''
            while 1:
                comments, next_page_token = youtube_spider.get_comments(video_id, out_fp,  page_token=next_page_token)
                json.dump(comments, out_fp, ensure_ascii=False)
                # 如果沒有下一頁留言，則跳離
                if not next_page_token:
                    break
            count = count + 1
        out_fp.close()
        channel_name = in_fp.readline()
        channel_name = channel_name.strip('\n')
    in_fp.close()

class YoutubeSpider():
    def __init__(self, api_key):
        self.base_url = "https://www.googleapis.com/youtube/v3/"
        self.api_key = api_key

    def get_html_to_json(self, path):
        """組合 URL 後 GET 網頁並轉換成 JSON"""
        api_url = f"{self.base_url}{path}&key={self.api_key}"
        r = requests.get(api_url)
        if r.status_code == requests.codes.ok:
            data = r.json()
        else:
            data = None
        return data

    def get_channel_uploads_id(self, channel_id, part='contentDetails'):
        """取得頻道上傳影片清單的ID"""
        path = f'channels?part={part}&id={channel_id}'
        data = self.get_html_to_json(path)
        try:
            uploads_id = data['items'][0]['contentDetails']['relatedPlaylists']['uploads']
        except KeyError:
            uploads_id = None
        return uploads_id

    def get_playlist(self, playlist_id, part='contentDetails', max_results=10):
        """從影片清單中獲取影片的ID"""
        path = f'playlistItems?part={part}&playlistId={playlist_id}&maxResults={max_results}'
        data = self.get_html_to_json(path)
        if not data:
            return []

        video_ids = []
        for data_item in data['items']:
            video_ids.append(data_item['contentDetails']['videoId'])
        return video_ids

    def get_comments(self, video_id, out_fp, page_token='', part='snippet', max_results=100):
        """取得影片留言"""
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
            
        return comments, next_page_token


if __name__ == "__main__":
    main()
