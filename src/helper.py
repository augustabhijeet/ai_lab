import base64
import mimetypes
from dotenv import load_dotenv, find_dotenv
import os

# import Anthropic
from anthropic import Anthropic

MODEL_NAME = "claude-haiku-4-5"

load_dotenv(find_dotenv())
if not os.getenv("ANTHROPIC_API_KEY"):
    raise ValueError("ANTHROPIC_API_KEY environment variable not set")

client = Anthropic()


def encode_image_to_base64(image_path: str) -> str:
    """
    Reads an image file and encodes it as a base64 string.

    Args:
        image_path (str): The path to the image file.
    Returns:
        str: The base64 encoded string of the image.
    """
    with open(image_path, "rb") as image_file:
        image_data = image_file.read()
        base64_image_string = base64.b64encode(image_data).decode("utf-8")
    return base64_image_string


def create_image_message(image_path):
    """
    Creates a message dictionary with both text and image content.

    Args:
        image_path (str): The path to the image file.
        text (str): The text content of the message.
    Returns:
        dict: A message dictionary containing the text and image content.
    """
    base64_image_string = encode_image_to_base64(image_path)
    media_type, _ = mimetypes.guess_type(image_path)

    image_block = {
        "type": "image",
        "source": {
            "type": "base64",
            "media_type": media_type,
            "data": base64_image_string
        }
    }
    return image_block

