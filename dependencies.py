import os
from fastapi import HTTPException, Header

def get_api_key():
    """
    Dependency that retrieves the API key from the environment variable.
    """
    stored_api_key = os.getenv("INDEED_API_KEY")
    if not stored_api_key:
        raise HTTPException(status_code=403, detail="No API Key found")
    return stored_api_key
