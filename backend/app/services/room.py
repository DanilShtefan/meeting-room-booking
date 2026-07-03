from datetime import date

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.booking import Booking
from app.models.room import Room
from app.models.slot import Slot
from app.schemas.room import RoomAvailability, RoomResponse


async def get_all_rooms(db: AsyncSession) -> list[RoomResponse]:
    result = await db.execute(select(Room).options(selectinload(Room.slots)))
    rooms = result.scalars().all()
    return [RoomResponse.model_validate(r) for r in rooms]


async def get_availability(
    db: AsyncSession, room_id: int, date: date
) -> RoomAvailability:
    result = await db.execute(
        select(Booking.slot_id).where(
            Booking.room_id == room_id, Booking.date == date
        )
    )
    booked_ids = [row[0] for row in result.all()]
    return RoomAvailability(room_id=room_id, date=date, booked_slot_ids=booked_ids)
