from datetime import date

from pydantic import BaseModel


class BookingCreate(BaseModel):
    room_id: int
    slot_id: int
    date: date


class BookingResponse(BaseModel):
    id: int
    room_id: int
    slot_id: int
    date: date
    user_id: int

    model_config = {"from_attributes": True}
