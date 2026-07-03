from httpx import AsyncClient


class TestRooms:
    async def test_list_rooms(self, client: AsyncClient, room_with_slots):
        response = await client.get("/api/v1/rooms/")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["name"] == "Test Room"
        assert data[0]["capacity"] == 10
        assert len(data[0]["slots"]) == 2

    async def test_list_rooms_empty(self, client: AsyncClient):
        response = await client.get("/api/v1/rooms/")
        assert response.status_code == 200
        assert response.json() == []

    async def test_room_availability_no_bookings(
        self, client: AsyncClient, room_with_slots
    ):
        response = await client.get(
            f"/api/v1/rooms/{room_with_slots.id}/availability",
            params={"date": "2026-07-10"},
        )
        assert response.status_code == 200
        data = response.json()
        assert data["room_id"] == room_with_slots.id
        assert data["booked_slot_ids"] == []
