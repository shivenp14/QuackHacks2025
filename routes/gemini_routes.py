from fastapi import APIRouter, Depends, File, Query, UploadFile
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

@router.post("/multimodal")
def gemini_multimodal_response(
    text: str = Query(...),
    file: UploadFile = File(None),
    api_key: str = Depends(get_gemini_api_key)
    ):
    """
    Endpoint to get a multimodal response from Gemini API based on user input and an optional file.
    """
    # Call the function that interacts with the Gemini API.
    result = gemini.gemini_multimodal_response(api_key, text, file)
    
    return result