from __future__ import annotations

from datetime import date

from sqlalchemy import Date, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Booking(Base):
    __tablename__ = "bookings"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    room_id: Mapped[int] = mapped_column(ForeignKey("rooms.id"), nullable=False)
    slot_id: Mapped[int] = mapped_column(ForeignKey("slots.id"), nullable=False)
    date: Mapped[date] = mapped_column(Date, nullable=False)

    user: Mapped[User] = relationship("User", back_populates="bookings")
    room: Mapped[Room] = relationship("Room", back_populates="bookings")
    slot: Mapped[Slot] = relationship("Slot", back_populates="bookings")
