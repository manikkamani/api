from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return {"status": "API is running"}

@app.get("/teams-notification")
def teams_notification():
    return {
        "recipient": "john@company.com",
        "message": "Please approve Invoice #123"
    }
