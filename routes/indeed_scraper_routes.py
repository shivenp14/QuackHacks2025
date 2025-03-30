from fastapi import APIRouter, Depends
from indeed_scraper.indeed_scraper import start_indeed_scraper
from dependencies import get_indeed_api_key

router = APIRouter()

@router.post("/scrape")
def scrape_indeed(location: str, position: str, api_key: str = Depends(get_indeed_api_key)):
    result = start_indeed_scraper(location, position, api_key)
    return {"message": "Scraping started", "result": result}