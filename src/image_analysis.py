import helper
from anthropic.types import TextBlock, MessageParam, ImageBlockParam, TextBlockParam

# create a message with both text and image content
image_block = helper.create_image_message(
    "/Users/abhijeetsrivastava/Development Projects/ai_lab/images/raindeer.webp"
)
content: list[TextBlockParam | ImageBlockParam] = [
    TextBlockParam(type="text", text="What does this image show?")
]
if image_block:
    content.append(ImageBlockParam(**image_block) if isinstance(image_block, dict) else image_block)

messages: list[MessageParam] = [
    {
        "role": "user",
        "content": content,
    }  # type: ignore
]

# execute the client

response = helper.client.messages.create(
    messages=messages,
    model=helper.MODEL_NAME,
    max_tokens=1024,
)

if isinstance(response.content[0], TextBlock):
    print(response.content[0].text)
else:
    print(f"Unexpected content type: {type(response.content[0])}")