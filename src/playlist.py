from src.api import Youtube
import isodate
import datetime


class PlayList:
    ''' плейлист '''
    youtube = None

    def __init__(self, playlist_id):
        ''' конструктор '''
        if PlayList.youtube is None:
            PlayList.youtube = Youtube().youtube
        self.__playlist_id = playlist_id
        # получить инфо о плейлисте
        self.title, self.url = self.__get_playlist_info()

        self.__total_duration = datetime.timedelta()
        self.__best_video_url = ''
        # получить инфо о видео
        self.__collect_video_infos()

    @property
    def total_duration(self):
        ''' вернуть длительность плейлиста '''
        return self.__total_duration

    def show_best_video(self):
        ''' ссылка на самое популярно видео '''
        return self.__best_video_url


    def __collect_video_infos(self):
        ''' получить всю информацию о видео из плейлиста '''
        like_count = 0
        max_likes = 0
        url = ''
        playlist_videos = PlayList.youtube.playlistItems().list(playlistId=self.__playlist_id,
                                                                part='contentDetails',
                                                                maxResults=50,
                                                                ).execute()
        video_ids = [video['contentDetails']['videoId'] for video in playlist_videos['items']]
        video_response = PlayList.youtube.videos().list(part='contentDetails,statistics',
                                                        id=','.join(video_ids)
                                                        ).execute()
        for video in video_response['items']:
            # YouTube video duration is in ISO 8601 format
            iso_8601_duration = video['contentDetails']['duration']
            self.__total_duration += isodate.parse_duration(iso_8601_duration)
            like_count = int(video['statistics']['likeCount'])
            if like_count > max_likes:
                url = ''.join(['https://youtu.be/', video['id']])
                max_likes = like_count
            self.__best_video_url = url

    def __get_playlist_info(self):
        ''' инфо о плейлисте '''
        title = ''
        url = ''
        snippet = PlayList.youtube.playlists().list(id=self.__playlist_id,
                                                    part='snippet',
                                                    maxResults=50,
                                                    ).execute()
        title = snippet['items'][0]['snippet']['title']
        url = ''.join(['https://www.youtube.com/playlist?list=', self.__playlist_id])
        return title, url
