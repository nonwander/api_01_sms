import os
import requests
import time

from dotenv import load_dotenv
from twilio.rest import Client

VER_API_VK = 5.92
URL_API_VK = 'https://api.vk.com/method/users.get'
load_dotenv()
account_sid = os.getenv('SID')
auth_token = os.getenv('TOKEN_TWILIO')
number_from = os.getenv('NUMBER_FROM')
number_to = os.getenv('NUMBER_TO')
token_vk = os.getenv('TOKEN_VK')
client = Client(account_sid, auth_token)


def get_status(user_id):
    params = {
        'access_token': token_vk,
        'user_ids': user_id,
        'fields': 'online',
        'v': VER_API_VK
    }
    try:
        status = requests.post(URL_API_VK, params=params).json()['response']
        return status[0]['online']
    except Exception:
        return 0


def send_sms(sms_text):
    message = client.messages.create(
        body=sms_text,
        from_=number_from,
        to=number_to,
    )
    return message.sid


if __name__ == '__main__':
    vk_id = input('Введите id ')
    while True:
        if get_status(vk_id) == 1:
            send_sms(f'{vk_id} сейчас онлайн!')
            break
        time.sleep(5)
