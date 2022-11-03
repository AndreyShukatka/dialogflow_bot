import random
from dotenv import load_dotenv
import os
import logging
from logger import BotLogsHandler

import vk_api as vk
from vk_api.longpoll import VkLongPoll, VkEventType
from dialogflow_helpers import detect_intent_texts


logger = logging.getLogger('telegram_logging')


def send_vk_msg(event, vk_api, project_id):
    session_id = event.user_id
    text = event.text
    answer = detect_intent_texts(project_id, text, session_id)
    if answer.query_result.fulfillment_text:
        vk_api.messages.send(
            user_id=session_id,
            message=answer.query_result.fulfillment_text,
            random_id=random.randint(1, 1000)
        )


if __name__ == "__main__":
    load_dotenv()
    print('Я тут vk')
    vk_token = os.environ['VK_TOKEN']
    vk_session = vk.VkApi(token=vk_token)
    vk_api = vk_session.get_api()
    project_id = os.environ['DIALOGFLOW_ID']
    longpoll = VkLongPoll(vk_session)
    logger = logging.getLogger('tg_Logger')
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO
    )
    logger.setLevel(logging.INFO)
    logger.addHandler(BotLogsHandler(os.environ['TGM_TOKEN'], os.environ['TGM_ID']))
    logger.info('VK бот запущен!')
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            send_vk_msg(event, vk_api, project_id)
