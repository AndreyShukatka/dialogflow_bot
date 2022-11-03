from google.cloud import dialogflow
from dotenv import load_dotenv
import os
import json


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
    for display_name in questions:
        training_phrases_parts = questions[display_name]['questions']
        message_texts = [questions[display_name]['answer']]
        create_intent(
            dialogflow_id,
            display_name,
            training_phrases_parts,
            message_texts)
