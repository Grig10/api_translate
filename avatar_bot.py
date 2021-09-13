import re
import json
import subprocess
import time
import webbrowser
import requests
import telebot
from requests.structures import CaseInsensitiveDict

import config

bot = telebot.TeleBot("1985018161:AAHzdQisPA_B0Tx9i48OegX139QbWGvpH4o")


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    if message.text == "/start":
        bot.send_message(message.chat.id, "Добро пожаловать,  {0.first_name}!\nЯ - {1.first_name}, переводчик русского "
                                          "жестового языка. "
                                          "Я буду переводить любую вашу фразу или слово в жесты. Напишите здесь.".format(
            message.from_user, bot.get_me()))
    elif message.text == "/help":
        bot.send_message(message.chat.id, "Напишите любую фразу или слово")


@bot.message_handler(content_types=['text'])
def translate_text(message):
    if re.search(r'[^а-я А-Я ?!."]', message.text):
        bot.send_message(message.chat.id, "Напишите только русскими буквами, пожалуйста")
    else:
        bot.send_message(message.chat.id, "Запрос отправлен. Ожидайте ответа, пожалуйста.")
        dict_avatar = json.loads(json.dumps(take_avatar()))
        id_streaming = dict_avatar["id"]
        url_streaming = dict_avatar["streaming_url"]
        if request_to_translate_text(id_streaming, url_streaming,
                                     message.text.strip()):
            video = open('video.mp4', 'rb')
            bot.send_video(message.chat.id, video, timeout=50)
        else:
            bot.send_message(message.chat.id, "Произошла ошибка с запросом. Повторите, пожалуйста.")


def request_to_translate_text(_id, _streaming, text):
    url_avatar = "http://84.201.181.102:8090/api/v1/avatar/" + _id + "/translate/text/"
    header = CaseInsensitiveDict()
    header["accept"] = "application/json"
    header["Content-Type"] = "application/json"
    resp_data = {"text": text, "speed": 1}
    response = requests.post(url_avatar, headers=header, json=resp_data)
    if response.status_code == 200:
        webbrowser.get('firefox').open(_streaming)
        proc = subprocess.Popen(
            [
                """ffmpeg -f avfoundation -i "1:0" -vf "crop=2500:1400:500:500" -pix_fmt yuv420p -y -r 10 video.mp4"""],
            shell=True)
        time.sleep(10)
        proc.terminate()
        time.sleep(5)
        return True
    else:
        return False


def take_avatar():
    url = "http://84.201.181.102:8090/api/v1/avatar/take/"
    headers = CaseInsensitiveDict()
    headers["accept"] = "application/json"
    resp = requests.get(url, headers=headers)
    if resp.status_code == 200:
        return resp.json()
    else:
        print("Received unexpected status code {}".format(resp.status_code))


if __name__ == '__main__':
        bot.polling(none_stop=True)
