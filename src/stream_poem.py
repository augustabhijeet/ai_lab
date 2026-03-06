import helper

# stream response
with helper.client.messages.stream(
    messages=[{"role": "user", "content": "Write a poem about the ocean"}], 
    model=helper.MODEL_NAME,
    max_tokens=1024,
) as stream:
    for text in stream.text_stream:
        print(text, end="")
        