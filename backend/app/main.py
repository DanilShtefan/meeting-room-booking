from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.auth import router as auth_router
from app.api.v1.rooms import router as rooms_router
from app.api.v1.bookings import router as bookings_router

app = FastAPI(title="Meeting Room Booking API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router, prefix="/api/v1")
app.include_router(rooms_router, prefix="/api/v1")
app.include_router(bookings_router, prefix="/api/v1")


@app.get("/health")
def health():
    return {"status": "ok"}
