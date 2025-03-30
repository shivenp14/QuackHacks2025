from fastapi import APIRouter, Depends
from indeed_scraper.indeed_scraper import start_indeed_scraper
from dependencies import get_indeed_api_key
from pydantic import BaseModel

router = APIRouter()

class JobSearchRequest(BaseModel):
    location: str
    position: str

@router.post("/scrape")
def scrape_indeed(request: JobSearchRequest, api_key: str = Depends(get_indeed_api_key)):
    result = start_indeed_scraper(request.location, request.position, api_key)
    return {"message": "Scraping started", "result": result}