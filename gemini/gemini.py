import base64
from typing import Optional
from fastapi import UploadFile
from pydantic import BaseModel
import requests
import json
from . import conversation_history, file
import json

class Listing(BaseModel):
    """
    Model for the listing data.
    """
    positionName: Optional[str] = None
    postedAt: Optional[str] = None
    company: Optional[str] = None
    location: Optional[str] = None
    description: Optional[str] = None

class Summarize(BaseModel):
    """
    Model for the description data.
    """
    content: str

class LikedListings(BaseModel):
    """
    Model for the liked listings data.
    """
    liked_listings: list[Listing]

def is_json_serializable(obj):
    try:
        json.dumps(obj)
        return True
    except TypeError:
        return False

def gemini_setup(api_key: str, request: Optional[LikedListings] = None):
    # Gemini 2.0 Flash REST endpoint. The endpoint URL uses the API key as a query parameter.
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={api_key}"

    prompt = open("gemini/prompt.txt", "r").read()
    if request is not None:
        request_json = request.model_dump_json()
        prompt = prompt + "\n\n Indeed Job Listings the User Chose :\n" + request_json
    
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

    return {"role": "assistant", "content": output}

def gemini_response(input:str, api_key:str):
    # Gemini 2.0 Flash REST endpoint. The endpoint URL uses the API key as a query parameter.
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={api_key}"

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

    return {"role": "assistant", "content": output}

def gemini_multimodal_response(api_key: str, text: str, uploaded_file: UploadFile = None):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={api_key}"

    # Build the base payload with text context.
    parts = [{"text": text}]

    mime_type = file.get_mime_type(uploaded_file.filename) if uploaded_file is not None else None
    has_file = False

    # If a file is provided, add it as a separate part.
    if mime_type is not None:
        file_content = uploaded_file.file.read()
        file_data = base64.b64encode(file_content).decode('utf-8')
        parts.append({
            "inlineData": {
                "mimeType": mime_type,
                "data": file_data
            }
        })
        has_file = True

    payload = {
        "contents": [
            {
                "role": "user",
                "parts": parts
            }
        ]
    }

    headers = {
        "Content-Type": "application/json"
    }

    response = requests.post(url, headers=headers, json=payload)
    result = response.json()
    print(json.dumps(result, indent=2))
    output = result["candidates"][0]["content"]["parts"][0]["text"]
    
    if has_file and file_data:
        conversation_history.add_message("user_file", file_data)
    conversation_history.add_message("user", text)
    conversation_history.add_message("assistant", output)
    conversation_history.save_history()

    return {"role": "assistant", "content": output}

def gemini_summarize(content: Summarize, api_key: str):
    # Gemini 2.0 Flash REST endpoint. The endpoint URL uses the API key as a query parameter.
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={api_key}"

    text = content.content
    # Create the JSON payload. Here we provide a single-turn query.
    payload = {
        "contents": [
            {
                "role": "user",
                "parts": [
                    {
                        "text": "Summarize the following: " + text
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

    return {"role": "assistant", "content": output}