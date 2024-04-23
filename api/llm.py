from api.prompt import Prompt

import os
from openai import OpenAI
client = OpenAI()

client.api_key = os.getenv("OPENAI_API_KEY")


class ChatGPT:
    """
    A class for generating responses using OpenAI's GPT model.

    Attributes:
    - prompt: an instance of the Prompt class for generating prompts
    - model: a string representing the name of the OpenAI model to use
    - temperature: a float representing the "creativity" of the responses generated
    - max_tokens: an integer representing the maximum number of tokens to generate in a response
    """

    def __init__(self):
        self.prompt = Prompt()
        self.model = os.getenv("OPENAI_MODEL", default = "gpt-4-turbo")
        self.temperature = float(os.getenv("OPENAI_TEMPERATURE", default = 0))
        self.max_tokens = int(os.getenv("OPENAI_MAX_TOKENS", default = 500))

    def get_response(self):
        """
        Generates a response using OpenAI's GPT model.

        Returns:
        - A string representing the generated response.
        """
        response = client.chat.completions.create(
            model=self.model,
            messages=self.prompt.generate_prompt(),
        )
        return response.choices[0].message.content

    def add_msg(self, text):
        """
        Adds a message to the prompt for generating a response.

        Parameters:
        - text: a string representing the message to add to the prompt.
        """
        self.prompt.add_msg(text)
