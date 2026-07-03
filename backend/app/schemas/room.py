from datetime import date, time

from pydantic import BaseModel


class SlotItem(BaseModel):
    id: int
    start_time: time
    end_time: time

    model_config = {"from_attributes": True}


class RoomResponse(BaseModel):
    id: int
    name: str
    capacity: int
    slots: list[SlotItem]

    model_config = {"from_attributes": True}


class RoomAvailability(BaseModel):
    room_id: int
    date: date
    booked_slot_ids: list[int]
