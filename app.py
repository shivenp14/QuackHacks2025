from fastapi import FastAPI
from routes.routers import router as main_router

app = FastAPI()

# Create a route that returns a JSON response
@app.get("/")
def testfunctionality():
    return {"message": "Success"}

#Include routers
app.include_router(main_router)