from src.api import Youtube


class Video:
    ''' Объект видео '''
    youtube = None

    def __init__(self, id_video):
        ''' создать объект по id '''
        if Video.youtube is None:
            Video.youtube = Youtube().youtube
        self.id_video = id_video
        video_response = Video.youtube.videos().list(
            part='snippet,statistics,contentDetails,topicDetails',
            id=id_video
        ).execute()
        self.title = video_response['items'][0]['snippet']['title']
        self.count_views = video_response['items'][0]['statistics']['viewCount']
        self.count_likes = video_response['items'][0]['statistics']['likeCount']
        self.comments = video_response['items'][0]['statistics']['commentCount']

    def __str__(self):
        ''' Название видео '''
        return self.title


class PLVideo(Video):
    ''' Объект видео из плейлиста'''
    def __init__(self, id_video, id_pl):
        ''' получить плейлист и создать из него объект видео по id '''
        if Video.youtube is None:
            Video.youtube = Youtube().youtube
        self.id_pl = id_pl
        playlist_videos = Video.youtube.playlistItems().list(playlistId=id_pl,
                                                             part='contentDetails',
                                                             maxResults=50,
                                                             ).execute()
        for video in playlist_videos['items']:
            if video['contentDetails']['videoId'] == id_video:
                super().__init__(id_video)
