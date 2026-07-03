from httpx import AsyncClient

from app.models.user import User, UserRole
from app.services.auth import hash_password


class TestBookings:
    async def test_create_booking(self, client: AsyncClient, user_token, room_with_slots):
        slot_id = room_with_slots.slots[0].id
        response = await client.post(
            "/api/v1/bookings/",
            json={
                "room_id": room_with_slots.id,
                "slot_id": slot_id,
                "date": "2026-07-10",
            },
            headers={"Authorization": f"Bearer {user_token}"},
        )
        assert response.status_code == 201
        data = response.json()
        assert data["room_id"] == room_with_slots.id
        assert data["slot_id"] == slot_id
        assert data["user_id"] is not None

    async def test_create_booking_without_auth(self, client: AsyncClient, room_with_slots):
        response = await client.post(
            "/api/v1/bookings/",
            json={
                "room_id": room_with_slots.id,
                "slot_id": room_with_slots.slots[0].id,
                "date": "2026-07-10",
            },
        )
        assert response.status_code == 401

    async def test_booking_conflict(self, client: AsyncClient, user_token, room_with_slots):
        slot_id = room_with_slots.slots[0].id
        await client.post(
            "/api/v1/bookings/",
            json={
                "room_id": room_with_slots.id,
                "slot_id": slot_id,
                "date": "2026-07-10",
            },
            headers={"Authorization": f"Bearer {user_token}"},
        )
        response = await client.post(
            "/api/v1/bookings/",
            json={
                "room_id": room_with_slots.id,
                "slot_id": slot_id,
                "date": "2026-07-10",
            },
            headers={"Authorization": f"Bearer {user_token}"},
        )
        assert response.status_code == 409
        assert response.json()["detail"] == "Slot is already booked for this date"

    async def test_cancel_own_booking(self, client: AsyncClient, user_token, booking):
        response = await client.delete(
            f"/api/v1/bookings/{booking.id}",
            headers={"Authorization": f"Bearer {user_token}"},
        )
        assert response.status_code == 204

    async def test_cancel_other_booking_returns_403(
        self, client: AsyncClient, booking, regular_user, db_session
    ):
        """a second regular user tries to cancel a booking that belongs to regular_user"""
        other = User(
            login="other",
            password_hash=hash_password("other"),
            full_name="Other",
            role=UserRole.user,
        )
        db_session.add(other)
        await db_session.commit()

        resp = await client.post(
            "/api/v1/auth/login",
            json={"login": "other", "password": "other"},
        )
        other_token = resp.json()["access_token"]

        response = await client.delete(
            f"/api/v1/bookings/{booking.id}",
            headers={"Authorization": f"Bearer {other_token}"},
        )
        assert response.status_code == 403

    async def test_admin_cancel_any_booking(
        self, client: AsyncClient, admin_token, booking
    ):
        response = await client.delete(
            f"/api/v1/bookings/{booking.id}",
            headers={"Authorization": f"Bearer {admin_token}"},
        )
        assert response.status_code == 204

    async def test_get_my_bookings(self, client: AsyncClient, user_token, booking):
        response = await client.get(
            "/api/v1/bookings/my",
            headers={"Authorization": f"Bearer {user_token}"},
        )
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["id"] == booking.id
