import requests
import re
from bs4 import BeautifulSoup
from translator import translate


def get_word_info(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
        'Referer': 'https://www.google.com'
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')

        title = soup.title.string
        title_parts = title.split('|')
        if len(title_parts) > 0:
            title = title_parts[0].strip().capitalize()

        definition = soup.find('div', class_='def ddef_d db')
        if definition is not None:
            definition = definition.text
        else:
            return None

        transcription_element = soup.find('span', class_='ipa dipa lpr-2 lpl-1')

        transcription = transcription_element.get_text()

        delldot = re.sub("=|.{2}$", '', definition)
        description = translate(delldot)

        return title, transcription, description
    except requests.exceptions.RequestException as e:
        return None, None, "Ошибка при запросе к серверу: "
