from fastapi import FastAPI

app = FastAPI(title="Meeting Room Booking API")


@app.get("/")
def root():
    return {"message": "Meeting Room Booking Service"}
