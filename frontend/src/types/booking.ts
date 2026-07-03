export interface Room {
  id: number
  name: string
  capacity: number
  slots: Slot[]
}

export interface Slot {
  start_time: string
  end_time: string
}

export interface Booking {
  id: number
  room_id: number
  slot_id: number
  date: string
  user_id: number
}

export interface LoginResponse {
  access_token: string
  token_type: string
}

export interface RoomAvailability {
  room_id: number
  date: string
  booked_slot_ids: number[]
}
