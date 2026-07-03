import asyncio

from app.database import async_session
from app.models.user import User, UserRole
from app.services.auth import hash_password


async def main() -> None:
    async with async_session() as session:
        admin = User(
            login="admin",
            password_hash=hash_password("admin"),
            full_name="Administrator",
            role=UserRole.admin,
        )
        user = User(
            login="user",
            password_hash=hash_password("user"),
            full_name="Regular User",
            role=UserRole.user,
        )
        session.add_all([admin, user])
        await session.commit()
        print("Test users created: admin/admin, user/user")


if __name__ == "__main__":
    asyncio.run(main())
