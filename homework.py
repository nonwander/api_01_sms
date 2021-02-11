import os
import time

import requests
from dotenv import load_dotenv
from twilio.rest import Client

load_dotenv()
account_sid = os.getenv('SID')
auth_token = os.getenv('TOKEN_TWILIO')
number_from = os.getenv('NUMBER_FROM')
number_to = os.getenv('NUMBER_TO')
client = Client(account_sid, auth_token)


def get_status(user_id):
    params = {
        'access_token': os.getenv('TOKEN_VK'),
        'user_ids': user_id,
        'fields': 'online',
        'v': 5.92
    }
    url_vk_api = 'https://api.vk.com/method/users.get'
    status = requests.post(url_vk_api, params=params)
    return status.json()['response'][0]['online']


def send_sms(sms_text):
    message = client.messages \
                    .create(
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
