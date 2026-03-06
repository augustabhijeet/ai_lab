import helper
from anthropic.types import TextBlock, MessageParam, ImageBlockParam, TextBlockParam

       
#try prompt caching

with (open("../files/frankenstein.txt", "r") as file):
    book_content = file.read()

def make_cached_api_call():
    messages: list[MessageParam] = [
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": "<book>" + book_content + "</book>",
                    "cache_control": {"type": "ephemeral"}
                },
                {
                    "type": "text",
                    "text": "Summarize the above book in 100 words."
                }
            ]
        }
    ]
    #track the time taken to execute the API call
    import time
    start_time = time.time()
    with helper.client.messages.stream(
        messages=messages,
        model=helper.MODEL_NAME,
        max_tokens=1024,
    ) as stream:
        for text in stream.text_stream:
            print(text, end="")
            
    end_time = time.time()
    print(f"Time taken: {end_time - start_time} seconds")
    
    return stream.get_final_message().usage, end_time - start_time

response1, duration1 = make_cached_api_call()
response2, duration2 = make_cached_api_call()

print("First call - Usage:", response1, "Duration:", duration1)
print("Second call - Usage:", response2, "Duration:", duration2)   