from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return {"status": "API is running"}

@app.get("/teams-notification")
def teams_notification():
    return {
        "recipient": "anirban_hati@epam.com",
        "message": "Ds project test"
    }
