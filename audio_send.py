import requests
from bs4 import BeautifulSoup
import telebot
from key_token import key

bot_token = key

bot = telebot.TeleBot(bot_token)


def download_and_send_audio(site_url, chat_id):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"}

    response = requests.get(site_url, headers=headers)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        audio_tag = soup.find('source', type="audio/mpeg")

        if audio_tag:
            audio_url = "https://dictionary.cambridge.org" + audio_tag['src']
            audio_response = requests.get(audio_url, headers=headers)
            if audio_response.status_code == 200:
                audio_data = audio_response.content

                bot.send_audio(chat_id, audio_data)
            else:
                return None
