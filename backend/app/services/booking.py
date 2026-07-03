from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.booking import Booking
from app.models.slot import Slot
from app.models.user import User, UserRole
from app.schemas.booking import BookingCreate, BookingResponse


class BookingService:
    @staticmethod
    async def create_booking(
        db: AsyncSession, user_id: int, data: BookingCreate
    ) -> BookingResponse:
        slot = await db.get(Slot, data.slot_id)
        if slot is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Slot not found",
            )

        if slot.room_id != data.room_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Slot does not belong to this room",
            )

        existing = await db.execute(
            select(Booking).where(
                Booking.room_id == data.room_id,
                Booking.slot_id == data.slot_id,
                Booking.date == data.date,
            )
        )
        if existing.scalar_one_or_none() is not None:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Slot is already booked for this date",
            )

        booking = Booking(
            user_id=user_id,
            room_id=data.room_id,
            slot_id=data.slot_id,
            date=data.date,
        )
        db.add(booking)
        await db.commit()
        await db.refresh(booking)
        return BookingResponse.model_validate(booking)

    @staticmethod
    async def cancel_booking(
        db: AsyncSession, booking_id: int, user: User
    ) -> None:
        booking = await db.get(Booking, booking_id)
        if booking is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Booking not found",
            )

        if booking.user_id != user.id and user.role != UserRole.admin:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Cannot cancel another user's booking",
            )

        await db.delete(booking)
        await db.commit()

    @staticmethod
    async def get_my_bookings(
        db: AsyncSession, user_id: int
    ) -> list[BookingResponse]:
        result = await db.execute(
            select(Booking).where(Booking.user_id == user_id)
        )
        bookings = result.scalars().all()
        return [BookingResponse.model_validate(b) for b in bookings]
