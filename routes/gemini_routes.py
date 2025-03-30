from fastapi import APIRouter, Depends, Query
from gemini import gemini
from dependencies import get_gemini_api_key

router = APIRouter()

@router.post("/setup")
def gemini_setup(api_key: str = Depends(get_gemini_api_key)):
    """
    Endpoint to get a response from Gemini API.
    """
    # Call the function that interacts with the Gemini API.
    result = gemini.gemini_setup(api_key)
    
    return result

@router.post("/response")
def gemini_response(
    input: str = Query(...),
    api_key: str = Depends(get_gemini_api_key)
    ):
    """
    Endpoint to get a response from Gemini API based on user input.
    """
    # Call the function that interacts with the Gemini API.
    result = gemini.gemini_response(input, api_key)
    
    return result