from api.prompt import Prompt
import os
from openai import OpenAI
import pyimgur

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
        self.model = os.getenv("OPENAI_MODEL", default="gpt-4")
        self.temperature = float(os.getenv("OPENAI_TEMPERATURE", default=0))
        self.max_tokens = int(os.getenv("OPENAI_MAX_TOKENS", default=600))

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

    def process_image_link(self, image_url):
        """
        Processes an image using OpenAI's image recognition capabilities.

        Parameters:
        - image_url: the URL of the image to be processed.

        Returns:
        - A dictionary representing the result of the image processing.
        """
        response = client.Completion.create(
            engine="davinci",
            prompt=f"Analyze the text in this image: {image_url}",
            max_tokens=100
        )
        return response

    def get_user_image(self, image_content):
        path = './static/temp.png'
        with open(path, 'wb') as fd:
            for chunk in image_content.iter_content():
                fd.write(chunk)
        return path

    def upload_img_link(self, imgpath):
        IMGUR_CLIENT_ID = os.getenv("IMGUR_CLIENT_ID")
        im = pyimgur.Imgur(IMGUR_CLIENT_ID)
        uploaded_image = im.upload_image(imgpath, title="Uploaded with PyImgur")
        return uploaded_image.link
