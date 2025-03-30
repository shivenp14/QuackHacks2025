from fastapi import APIRouter
from .indeed_scraper_routes import router as indeed_router
#from .gemini_routes import router as gemini_router

router = APIRouter()

# Include individual routers with their own prefixes and tags
router.include_router(indeed_router, prefix="/indeed", tags=["Indeed Scraper"])
# router.include_router(gemini, prefix="/gemini", tags=["Gemini"])