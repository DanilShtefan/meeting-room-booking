from __future__ import annotations

from sqlalchemy import ForeignKey, Time
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Slot(Base):
    __tablename__ = "slots"

    id: Mapped[int] = mapped_column(primary_key=True)
    room_id: Mapped[int] = mapped_column(ForeignKey("rooms.id"), nullable=False)
    start_time: Mapped[Time] = mapped_column(Time, nullable=False)
    end_time: Mapped[Time] = mapped_column(Time, nullable=False)

    room: Mapped[Room] = relationship("Room", back_populates="slots")
    bookings: Mapped[list[Booking]] = relationship("Booking", back_populates="slot")
