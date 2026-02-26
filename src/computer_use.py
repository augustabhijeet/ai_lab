#import Anthropic
from anthropic import Anthropic

#load environment variables
from dotenv import load_dotenv
import os
load_dotenv()

MODEL_NAME = "claude-3-5-sonnet-20241022"

client = Anthropic(
    # This is the default and can be omitted
    api_key=os.getenv("ANTHROPIC_API_KEY"),
)
