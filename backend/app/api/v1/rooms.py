from datetime import date

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.schemas.room import RoomAvailability, RoomResponse
from app.services.room import get_all_rooms, get_availability

router = APIRouter(prefix="/rooms", tags=["rooms"])


@router.get("/", response_model=list[RoomResponse])
async def list_rooms(db: AsyncSession = Depends(get_db)):
    return await get_all_rooms(db)


@router.get("/{room_id}/availability", response_model=RoomAvailability)
async def room_availability(
    room_id: int,
    date: date = Query(...),
    db: AsyncSession = Depends(get_db),
):
    return await get_availability(db, room_id, date)
