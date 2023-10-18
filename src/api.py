import os
from dotenv import load_dotenv
from googleapiclient.discovery import build


class Api:
    def __init__(self):
        self.__api_key = Api.__get_api_key()

    @staticmethod
    def __get_api_key():
        '''
        Считать API_KEY из переменных окружения
        '''
        api_key = ''
        current_dir = os.path.dirname(os.path.abspath(__file__))
        root_dir = os.path.split(current_dir)[0]
        filepath = os.path.join(root_dir, '.env')
        if os.path.exists(filepath):
            load_dotenv(filepath)
            api_key = os.getenv('API_KEY')
        return api_key

    @property
    def api_key(self):
        return self.__api_key


class Youtube:
    def __init__(self):
        self.__service = build('youtube', 'v3', developerKey=Api().api_key)

    @property
    def youtube(self):
        return self.__service
