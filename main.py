from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return {"status": "API is running"}

@app.get("/teams-notification")
def teams_notification():
    return {
    "recipient": [
        "anirban_hati@epam.com",
        "manikkamani_subramani@epam.com",
        "saran_kaanthl@epam.com"
    ],
    "message": [
        "Hi anirban DS project test",
        "Hi manikkamani DS project test",
        "Hi saran DS project test"
    ]
}
