from __future__ import annotations

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Room(Base):
    __tablename__ = "rooms"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    capacity: Mapped[int] = mapped_column(nullable=False)

    slots: Mapped[list[Slot]] = relationship("Slot", back_populates="room")
    bookings: Mapped[list[Booking]] = relationship("Booking", back_populates="room")
