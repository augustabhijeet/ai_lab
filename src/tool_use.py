import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import helper
from files.fake_database import FakeDatabase

db = FakeDatabase()

#defind tools schema
tools: list = [
    {
        "name": "get_customer",
        "description": "Retrieve customer information based on customer ID or email",
        "input_schema": {
            "type": "object",
            "properties": {
                "key": {"type": "string", "enum": ["id", "email"], "description": "The key to search by (e.g., 'id' or 'email')"},
                "value": {"type": "string", "description": "The value to search for (e.g., '1' or 'john@example.com')"}
            }
        }
    },
    {
        "name": "get_order",
        "description": "Retrieve order information based on order ID or customer ID",
        "input_schema": {
            "type": "object",
            "properties": {
                "key": {"type": "string", "enum": ["id", "customer_id"], "description": "The key to search by (e.g., 'id' or 'customer_id')"},
                "value": {"type": "string", "description": "The value to search for (e.g., '1' or '2')"}
            }
        }
    }
]

messages: list = [
    {"role": "user", "content": "Get information for customer with ID 2"}
]
        

def call_tool(tool_name: str, tool_input: dict):
    if tool_name == "get_customer":
        print(f"Calling get_customer with input: {tool_input}")
        return db.get_customer(tool_input["key"], tool_input["value"])
    elif tool_name == "get_order":
        print(f"Calling get_order with input: {tool_input}")
        return db.get_order(tool_input["key"], tool_input["value"])
    else:
        raise ValueError(f"Unknown tool: {tool_name}")
    
    

