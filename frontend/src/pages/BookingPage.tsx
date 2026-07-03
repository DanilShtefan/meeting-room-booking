import { useEffect, useState } from 'react'
import { useAuth } from '../context/AuthContext'
import client from '../api/client'
import type { Booking, Room, RoomAvailability } from '../types/booking'
import './BookingPage.css'

function BookingPage() {
  const { logout } = useAuth()
  const today = new Date().toISOString().slice(0, 10)

  const [date, setDate] = useState(today)
  const [rooms, setRooms] = useState<Room[]>([])
  const [selectedRoomId, setSelectedRoomId] = useState<number | null>(null)
  const [availability, setAvailability] = useState<RoomAvailability | null>(null)
  const [myBookings, setMyBookings] = useState<Booking[]>([])
  const [error, setError] = useState('')

  useEffect(() => {
    client.get<Room[]>('/rooms/').then(({ data }) => setRooms(data))
  }, [])

  useEffect(() => {
    setAvailability(null)
    if (selectedRoomId === null) return
    client
      .get<RoomAvailability>(`/rooms/${selectedRoomId}/availability`, {
        params: { date },
      })
      .then(({ data }) => setAvailability(data))
  }, [selectedRoomId, date])

  useEffect(() => {
    fetchMyBookings()
  }, [])

  const fetchMyBookings = () => {
    client.get<Booking[]>('/bookings/my').then(({ data }) => setMyBookings(data))
  }

  const selectedRoom = rooms.find((r) => r.id === selectedRoomId)

  const handleBook = async (slotId: number) => {
    if (!selectedRoomId) return
    setError('')
    try {
      await client.post('/bookings/', {
        room_id: selectedRoomId,
        slot_id: slotId,
        date,
      })
      fetchMyBookings()
      const { data } = await client.get<RoomAvailability>(
        `/rooms/${selectedRoomId}/availability`,
        { params: { date } },
      )
      setAvailability(data)
    } catch {
      setError('Failed to create booking')
    }
  }

  const handleCancel = async (bookingId: number) => {
    setError('')
    try {
      await client.delete(`/bookings/${bookingId}`)
      fetchMyBookings()
      if (selectedRoomId !== null) {
        const { data } = await client.get<RoomAvailability>(
          `/rooms/${selectedRoomId}/availability`,
          { params: { date } },
        )
        setAvailability(data)
      }
    } catch {
      setError('Failed to cancel booking')
    }
  }

  const isSlotBooked = (slotId: number) =>
    availability?.booked_slot_ids.includes(slotId) ?? false

  return (
    <div className="booking-page">
      <header className="booking-header">
        <h1>Meeting Room Booking</h1>
        <button className="logout-btn" onClick={logout}>
          Logout
        </button>
      </header>

      {error && <p className="booking-error">{error}</p>}

      <div className="date-picker">
        <label>Date</label>
        <input
          type="date"
          value={date}
          onChange={(e) => setDate(e.target.value)}
        />
      </div>

      <section>
        <h2>Rooms</h2>
        <div className="rooms-grid">
          {rooms.map((room) => (
            <button
              key={room.id}
              className={`room-card ${selectedRoomId === room.id ? 'selected' : ''}`}
              onClick={() => setSelectedRoomId(room.id)}
            >
              <strong>{room.name}</strong>
              <span>Capacity: {room.capacity}</span>
            </button>
          ))}
        </div>
      </section>

      {selectedRoom && (
        <section>
          <h2>Slots — {selectedRoom.name}</h2>
          <div className="slots-grid">
            {selectedRoom.slots.map((slot) => {
              const booked = isSlotBooked(slot.id)
              return (
                <div
                  key={slot.id}
                  className={`slot-card ${booked ? 'booked' : ''}`}
                >
                  <span>
                    {slot.start_time.slice(0, 5)}–{slot.end_time.slice(0, 5)}
                  </span>
                  <button
                    disabled={booked}
                    onClick={() => handleBook(slot.id)}
                  >
                    {booked ? 'Booked' : 'Book'}
                  </button>
                </div>
              )
            })}
          </div>
        </section>
      )}

      <section>
        <h2>My Bookings</h2>
        {myBookings.length === 0 && <p className="empty">No bookings yet</p>}
        <div className="bookings-list">
          {myBookings.map((b) => {
            const room = rooms.find((r) => r.id === b.room_id)
            const slot = room?.slots.find((s) => s.id === b.slot_id)
            const time = slot
              ? `${slot.start_time.slice(0, 5)}–${slot.end_time.slice(0, 5)}`
              : `Slot ${b.slot_id}`
            return (
              <div key={b.id} className="booking-item">
                <span>
                  {room?.name ?? `Room ${b.room_id}`} — {b.date} — {time}
                </span>
                <button onClick={() => handleCancel(b.id)}>Cancel</button>
              </div>
            )
          })}
        </div>
      </section>
    </div>
  )
}

export default BookingPage
