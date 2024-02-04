import openai


class AI:

    def __init__(self, settings):
        openai.api_key = settings['API_KEY']  # APIkey
        openai.Model.list()

    @staticmethod
    def chat(message):
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": f"{message}"}
            ]
        )
        chat_response = completion.choices[0].message.content
        return chat_response

    @staticmethod
    def chatSys(message):
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": f"{message}"}
            ]
        )
        chat_response = completion.choices[0].message.content
        return chat_response
