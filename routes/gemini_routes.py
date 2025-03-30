from typing import Optional
from fastapi import APIRouter, Depends, File, Query, UploadFile
from pydantic import BaseModel
from gemini import gemini, conversation_history
from dependencies import get_gemini_api_key

router = APIRouter()

class Listing(BaseModel):
    """
    Model for the listing data.
    """
    positionName: Optional[str] = None
    postedAt: Optional[str] = None
    company: Optional[str] = None
    location: Optional[str] = None
    description: Optional[str] = None

class LikedListings(BaseModel):
    """
    Model for the liked listings data.
    """
    liked_listings: list[Listing]

@router.post("/setup")
def gemini_setup(request: Optional[LikedListings] = None, api_key: str = Depends(get_gemini_api_key)):
    """
    Endpoint to get a response from Gemini API.
    """
    # Call the function that interacts with the Gemini API.
    result = gemini.gemini_setup(api_key, request)
    
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

@router.get("/history")
def get_history():
    """
    Endpoint to retrieve the conversation history.
    """
    # Call the function that retrieves the conversation history.
    history = conversation_history.get_history()
    
    return {"history": history}