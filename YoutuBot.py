token = "695344585:AAGcqOuvRDaAUHYCMWwno4W5tz35-UTWgfg"

import requests  
from bs4 import BeautifulSoup
#from flask import Flask
#import os

#server = Flask(__name__)

class BotHandler:

    def __init__(self, token):
        self.token = token
        self.api_url = "https://api.telegram.org/bot{}/".format(token)

    def get_updates(self, offset=None, timeout=30):
        method = 'getUpdates'
        params = {'timeout': timeout, 'offset': offset}
        resp = requests.get(self.api_url + method, params)
        result_json = resp.json()
        if 'result' in result_json:
            result_json = resp.json()['result']
        else:
            result_json = ''
        return result_json

    def send_message(self, chat_id, text):
        params = {'chat_id': chat_id, 'text': text}
        method = 'sendMessage'
        resp = requests.post(self.api_url + method, params)
        return resp

    def get_last_update(self):
        get_result = self.get_updates()

        if len(get_result) > 0:
            last_update = get_result[-1]
        else:
            last_update = None
        #    last_update = get_result[len(get_result)]

        return last_update

    def get_text(self, update):
        if 'text' in update['message']:
            return update['message']['text']
        else:
            return None

    def get_chat_id(self, update):
        return update['message']['chat']['id']

    def get_update_id(self, update):
        return update['update_id']
        
    def check_inline_query(self):
        if "inline_query" in update:
            return True
        else:
            return False

    def search_on_youtube(self, text):
        search_url = "https://www.youtube.com/results"
        params = {'search_query': text}
        resp = requests.get(search_url, params)
        soup = BeautifulSoup(resp.text, 'html.parser')
        div = soup.find(attrs={ "class" : "yt-uix-tile-link"})
        if div:
            final_url = "https://www.youtube.com" + div['href']
        else:
            final_url = None
        return final_url
    
    def parse_msg_text(self, text):
        if "/start" in text:
            msg = "Привет, я бот для поиска видео на youtube. Просто напиши мне что искать!"
        elif "/help" in text:
            msg = "Просто напиши мне что искать, и я найду тебе видосик!"
        else:
            found_url = self.search_on_youtube(text)
            if found_url:
                msg = "А вот и твой видосик: " + found_url
            else:
                msg = "К сожалению, я ничего не нашел("
        return msg


def main():
    new_offset = None
    while True:
        TestBot = BotHandler(token)
        TestBot.get_updates(new_offset)
        last_update = TestBot.get_last_update()
        if last_update:
            chat_id = TestBot.get_chat_id(last_update)
            msg_text = TestBot.get_text(last_update)
            update_id = TestBot.get_update_id(last_update)
            if msg_text:
                msg = TestBot.parse_msg_text(msg_text)
                TestBot.send_message(chat_id, msg)
            new_offset = update_id + 1

if __name__ == '__main__':  
    try:
        #server.run(host="0.0.0.0", port=os.environ.get('PORT', 5000))
        #server = Flask(__name__)
        main()
    except KeyboardInterrupt:
        exit()