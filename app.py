from fastapi import FastAPI
from routes.routers import router as main_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Create a route that returns a JSON response
@app.get("/")
def testfunctionality():
    return {"message": "Success"}


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Adjust if frontend URL is different
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods
    allow_headers=["*"],  # Allow all headers
)

#Include routers
app.include_router(main_router)