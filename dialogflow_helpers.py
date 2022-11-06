from google.cloud import dialogflow
from dotenv import load_dotenv
import os
import json


def detect_intent_texts(project_id, text: str, session_id):
    language_code = 'ru'
    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(project_id, session_id)
    text_input = dialogflow.TextInput(text=text, language_code=language_code)
    query_input = dialogflow.QueryInput(text=text_input)
    response = session_client.detect_intent(
        request={"session": session, "query_input": query_input}
    )
    return response


def create_intent(
        dialogflow_id,
        display_name,
        training_phrases_parts,
        message_texts
):
    intents_client = dialogflow.IntentsClient()
    parent = dialogflow.AgentsClient.agent_path(dialogflow_id)
    training_phrases = []
    for training_phrases_part in training_phrases_parts:
        part = dialogflow.Intent.TrainingPhrase.Part(
            text=training_phrases_part
        )
        training_phrase = dialogflow.Intent.TrainingPhrase(parts=[part])
        training_phrases.append(training_phrase)
    text = dialogflow.Intent.Message.Text(text=message_texts)
    message = dialogflow.Intent.Message(text=text)
    intent = dialogflow.Intent(
        display_name=display_name,
        training_phrases=training_phrases,
        messages=[message]
    )

    intents_client.create_intent(
        request={"parent": parent, "intent": intent}
    )


if __name__ == '__main__':
    load_dotenv()
    with open('questions.json', 'r', encoding='utf-8') as file:
        questions = file.read()
    questions = json.loads(questions)
    dialogflow_id = os.environ['DIALOGFLOW_ID']
    for display_name, question in questions.items():
        training_phrases_parts = question['questions']
        message_texts = [question['answer']]
        create_intent(
            dialogflow_id,
            display_name,
            training_phrases_parts,
            message_texts)
