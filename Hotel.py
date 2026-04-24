class Hotel:
    def __init__(self, name):
        if not name.strip():
            raise ValueError("Hotel name cannot be empty.")
        self.name = name.strip()
        self.rooms = []
        self.guests = []
        self.reservations = []

    def add_room(self, room):
        if any(existing.number == room.number for existing in self.rooms):
            raise ValueError("Room with this number already exists.")
        self.rooms.append(room)

    def add_guest(self, guest):
        if any(existing.guest_id == guest.guest_id for existing in self.guests):
            raise ValueError("Guest with this ID already exists.")
        self.guests.append(guest)

    def get_free_rooms(self):
        return [room for room in self.rooms if room.available]

    def find_guest(self, guest_id):
        return next((g for g in self.guests if g.guest_id == guest_id), None)

    def find_room(self, room_number):
        return next((r for r in self.rooms if r.number == room_number), None)

    def find_reservation(self, reservation_id):
        return next((r for r in self.reservations if r.reservation_id == reservation_id), None)

    def create_reservation(self, guest_id, room_number, nights):
        guest = self.find_guest(guest_id)
        room = self.find_room(room_number)
        if guest is None:
            raise ValueError("Guest not found.")
        if room is None:
            raise ValueError("Room not found.")
        if not room.available:
            raise ValueError("Room is not available.")

        reservation = Reservation(len(self.reservations) + 1, guest, room, nights)
        self.reservations.append(reservation)
        return reservation

    def cancel_reservation(self, reservation_id):
        reservation = self.find_reservation(reservation_id)
        if reservation is None:
            raise ValueError("Reservation not found.")
        reservation.cancel()

    def check_in_guest(self, reservation_id):
        reservation = self.find_reservation(reservation_id)
        if reservation is None:
            raise ValueError("Reservation not found.")
        reservation.check_in()

    def check_out_guest(self, reservation_id):
        reservation = self.find_reservation(reservation_id)
        if reservation is None:
            raise ValueError("Reservation not found.")
        reservation.check_out()

    def total_revenue(self):
        return sum(
            reservation.total()
            for reservation in self.reservations
            if reservation.checked_out and not reservation.is_cancelled
        )
