import requests
import json
from . import conversation_history
import json

def is_json_serializable(obj):
    try:
        json.dumps(obj)
        return True
    except TypeError:
        return False

def gemini_setup(api_key: str):
    # Gemini 2.0 Flash REST endpoint. The endpoint URL uses the API key as a query parameter.
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={api_key}"

    prompt = open("gemini/prompt.txt", "r").read()

    # Create the JSON payload. Here we provide a single-turn query.
    payload = {
        "contents": [
            {
                "role": "user",
                "parts": [
                    {
                        "text": prompt
                    }
                ]
            }
        ]
    }

    # Set the appropriate header.
    headers = {
        "Content-Type": "application/json"
    }

    # Make the POST request.
    response = requests.post(url, headers=headers, json=payload)

    # Print out the response JSON.
    result = response.json()

    output = result["candidates"][0]["content"]["parts"][0]["text"]

    conversation_history.add_message("user", prompt)
    conversation_history.add_message("assistant", output)
    conversation_history.save_history()
    print(conversation_history.get_history())

    return {"role": "assistant", "content": output}

def gemini_response(input:str, api_key:str):
    # Gemini 2.0 Flash REST endpoint. The endpoint URL uses the API key as a query parameter.
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={api_key}"
    print(is_json_serializable(conversation_history.get_history()))
    print(conversation_history.get_history())

    # Create the JSON payload. Here we provide a single-turn query.
    payload = {
        "contents": [
            {
                "role": "user",
                "parts": [
                    {
                        "text": json.dumps(conversation_history.get_history(), indent=2) + input
                    }
                ]
            }
        ]
    }

    # Set the appropriate header.
    headers = {
        "Content-Type": "application/json"
    }

    # Make the POST request.
    response = requests.post(url, headers=headers, json=payload)

    # Print out the response JSON.
    result = response.json()
    output = result["candidates"][0]["content"]["parts"][0]["text"]

    conversation_history.add_message("user", input)
    conversation_history.add_message("assistant", output)
    conversation_history.save_history()

    print(conversation_history.get_history())

    return {"role": "assistant", "content": output}