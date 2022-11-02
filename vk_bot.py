import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
import os
from dotenv import load_dotenv
import random


def vk_bot(vk_token):
    vk_session = vk_api.VkApi(token=vk_token)
    vk = vk_session.get_api()
    longpoll = VkLongPoll(vk_session)
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW:
            print('Новое сообщение:')
            if event.to_me:
                print('Для меня от: ', event.user_id)
                vk.messages.send(user_id=event.user_id, message=event.text, random_id=random.randint(1, 1000))
            else:
                print('От меня для: ', event.user_id)
            print('Текст:', event.text)


def main():
    load_dotenv()
    vk_token = os.environ['VK_TOKEN']
    vk_bot(vk_token)


if __name__ == '__main__':
    main()
