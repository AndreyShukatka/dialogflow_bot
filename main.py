from dotenv import load_dotenv
from telegram import Update
from telegram.ext import CallbackContext, CommandHandler, Updater, MessageHandler, Filters
from google.cloud import dialogflow
import os


def detect_intent_texts(update: Update, context: CallbackContext):
    language_code = 'ru'
    session_client = dialogflow.SessionsClient()
    text = update.message.text
    project_id = os.environ['DIALOGFLOW_ID']
    session_id = update.effective_chat.id
    session = session_client.session_path(project_id, session_id)
    text_input = dialogflow.TextInput(text=text, language_code=language_code)
    query_input = dialogflow.QueryInput(text=text_input)
    response = session_client.detect_intent(
        request={"session": session, "query_input": query_input}
    )
    context.bot.send_message(chat_id=session_id, text=response.query_result.fulfillment_text)


def start(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Привет")


def main():
    load_dotenv()
    tg_token = os.environ['TELEGRAM_TOKEN']
    updater = Updater(token=tg_token)
    project_id = os.environ['DIALOGFLOW_ID']
    session_id = os.environ['SESSION_ID']
    language_code = 'ru'
    dispatcher = updater.dispatcher
    start_handler = CommandHandler('start', start)
    dispatcher.add_handler(start_handler)
    echo_handler = MessageHandler(Filters.text & (~Filters.command), detect_intent_texts)
    dispatcher.add_handler(echo_handler)
    updater.start_polling()


if __name__ == '__main__':
    main()