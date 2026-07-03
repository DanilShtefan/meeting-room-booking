import asyncio
from datetime import time

from sqlalchemy import select

from app.database import async_session
from app.models.room import Room
from app.models.slot import Slot
from app.models.user import User, UserRole
from app.services.auth import hash_password


async def main() -> None:
    async with async_session() as session:
        result = await session.execute(select(User).where(User.login == "admin"))
        admin = result.scalar_one_or_none()
        if not admin:
            admin = User(
                login="admin",
                password_hash=hash_password("admin"),
                full_name="Administrator",
                role=UserRole.admin,
            )
            session.add(admin)

        result = await session.execute(select(User).where(User.login == "user"))
        user = result.scalar_one_or_none()
        if not user:
            user = User(
                login="user",
                password_hash=hash_password("user"),
                full_name="Regular User",
                role=UserRole.user,
            )
            session.add(user)

        await session.flush()
        print("Test users ready: admin/admin, user/user")

        rooms_data = [
            Room(name="Конференц-зал А", capacity=10),
            Room(name="Переговорка B", capacity=4),
            Room(name="Лаунж C", capacity=6),
        ]

        slots_data = []
        for h in range(9, 19):
            slots_data.append(Slot(start_time=time(h, 0), end_time=time(h + 1, 0)))

        for room in rooms_data:
            result = await session.execute(
                select(Room).where(Room.name == room.name)
            )
            existing = result.scalar_one_or_none()
            if existing:
                room = existing
            else:
                session.add(room)
                await session.flush()

            for slot in slots_data:
                result = await session.execute(
                    select(Slot).where(
                        Slot.room_id == room.id,
                        Slot.start_time == slot.start_time,
                    )
                )
                if not result.scalar_one_or_none():
                    new_slot = Slot(
                        room_id=room.id,
                        start_time=slot.start_time,
                        end_time=slot.end_time,
                    )
                    session.add(new_slot)

        await session.commit()
        print("Rooms and slots created")


if __name__ == "__main__":
    asyncio.run(main())
