import openai



class AI:

    def __init__(self, settings):
        openai.api_key = settings['API_KEY']

    @staticmethod
    def chat(message, context):
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": message + context}
            ]
        )
        chat_response = completion.choices[0].text
        return chat_response
