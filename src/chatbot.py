import re
from urllib import response
import helper
from helper import client, MODEL_NAME
from tool_use import tools, call_tool

from anthropic.types import TextBlock, MessageParam, ImageBlockParam, TextBlockParam, ToolUseBlock

def extract_reply(text):
    """
    Extracts the content within <reply></reply> tags from the given text.

    Args:
        text (str): The input text containing the reply.

    Returns:
        str: The extracted reply content.
    """
    match = re.search(r"<reply>(.*?)</reply>", text, re.DOTALL)
    if match:
        return match.group(1).strip()
    return text

def simple_chat():
    system_prompt = """You are a customer support chat bot for an online retailer.
    Your job is to help users look up their account and order information.
    Be helpful and brief in your responses.
    You have access to a set of tools, but only use them when needed.  
    If you do not have enough information to use a tool correctly, 
    ask a user follow up questions to get the required inputs.
    Do not call any of the tools unless you have the required 
    data from a user. 

    In each conversational turn, you will begin by thinking about 
    your response. Once you're done, you will write a user-facing 
    response. It's important to place all user-facing conversational 
    responses in <reply></reply> XML tags to make them easy to parse.
    """
    user_message = input("\nUser: ")
    messages: list = [
        {"role": "user", "content": user_message}
    ]
    while True:
        if user_message.lower() in ["exit", "quit"]:
            print("Exiting chat. Goodbye!")
            break
        
        #If the last message is from the assistant, 
        # get another input from the user
        if messages[-1]["role"] == "assistant":
            user_message = input("\nUser: ")
            messages.append({"role": "user", "content": user_message})
            
        #Call the model to get a response
        response = helper.client.messages.create(
            model=MODEL_NAME,
            system=system_prompt,
            messages=messages,
            tools=tools,
            max_tokens=1000
        ) 
            
            
        if response.stop_reason == "tool_use":
            messages.append({"role": "assistant", "content": response.content})
            tool_use = response.content[-1]
            if isinstance(tool_use, ToolUseBlock):
                tool_name = tool_use.name
                tool_input = tool_use.input
                print(f"\n[Model calling tool]: {tool_name} with input {tool_input})\n")
                tool_output = call_tool(tool_name, tool_input)
                print(f"\n[Tool output]: {tool_output}\n")
                # Add the tool output to the messages so that Claude can see it in the next turn
                messages.append(
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "tool_result",
                                "tool_use_id": tool_use.id,
                                "content": str(tool_output)
                            },
                        ]
                    }
                )   
        
        else:
            if isinstance(response.content[0], TextBlock):
                model_reply = extract_reply(response.content[0].text)
                print(f"\nClaude: {model_reply}\n")
                messages.append({"role": "assistant", "content": response.content[0].text})
            else:
                print(f"Unexpected content type: {type(response.content[0])}")
                    
                    
                
simple_chat()