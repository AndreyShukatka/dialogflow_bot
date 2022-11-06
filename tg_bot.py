from dotenv import load_dotenv
from telegram import Update
from telegram.ext import CallbackContext, CommandHandler, Updater, MessageHandler, Filters
from dialogflow_helpers import detect_intent_texts
import os
import logging
from logger import BotLogsHandler

logger = logging.getLogger('tg_Logger')


def start(update: Update, context: CallbackContext):
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Здравствуйте! Чем могу вам помочь?"
    )


def send_tgm_msg(update: Update, context: CallbackContext):
    project_id = os.environ['DIALOGFLOW_ID']
    text = update.message.text
    session_id = update.message.chat_id
    answer = detect_intent_texts(project_id, text, session_id)
    if answer.query_result.fulfillment_text:
        context.bot.send_message(
            chat_id=session_id,
            text=answer.query_result.fulfillment_text
        )


def main():
    load_dotenv()
    tg_token = os.environ['TGM_TOKEN']
    tgm_id = os.environ['TGM_ID']
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO
    )
    logger.setLevel(logging.INFO)
    logger.addHandler(BotLogsHandler(tg_token, tgm_id))
    logger.info('Телеграмм бот запущен!')
    updater = Updater(token=tg_token)
    dispatcher = updater.dispatcher
    start_handler = CommandHandler('start', start)
    dispatcher.add_handler(start_handler)
    echo_handler = MessageHandler(
        Filters.text & (~Filters.command),
        send_tgm_msg
    )
    dispatcher.add_handler(echo_handler)
    updater.start_polling()


if __name__ == '__main__':
    main()
