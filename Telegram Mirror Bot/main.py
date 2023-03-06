from urllib.parse import quote, unquote
from urllib.request import urlopen
import json
import time


class Bot:
    base_url = r"https://api.telegram.org/bot{token}/"

    def __init__(self, token, delay=3):
        if not Bot.check_token(token):
            raise ValueError('Entered token is not valid!')

        self.url = Bot.base_url.format(token=token)
        self.delay = delay
        self.updates = {}

    def start(self):
        while True:
            if self.check_updates():
                message = self.updates['result'][0]['message']
                if 'text' in message:
                    chat_id = str(message['chat']['id'])
                    self.send_message(message['text'], chat_id)
                else:
                    self.offset()

            time.sleep(self.delay)

    def send_message(self, text, chat_id):
        text = quote(text.encode('utf-8'))
        response = Bot.fetch_url(self.url + f'sendMessage?chat_id={chat_id}&text={text}')
        if response['ok']:
            self.offset()

    def offset(self):
        update_id = self.updates['result'][0]['update_id']
        urlopen(self.url + f'getUpdates?offset={update_id+1}')

    def check_updates(self):
        self.updates = Bot.fetch_url(self.url + 'getUpdates')
        return self.updates['result']

    @staticmethod
    def check_token(token):
        result = Bot.fetch_url(Bot.base_url.format(token=token) + 'getme')
        return result['ok'] and result['result']['is_bot']

    @staticmethod
    def fetch_url(url, encoding='utf-8'):
        return json.loads(urlopen(url).read().decode(encoding))



TOKEN = 'your token'


if __name__ == "__main__":
    bot = Bot(TOKEN)
    bot.start()
