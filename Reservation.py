class Reservation:
    def __init__(self, reservation_id, guest, room, nights):
        if reservation_id <= 0:
            raise ValueError("Reservation ID must be positive.")
        if nights <= 0:
            raise ValueError("Nights must be greater than 0.")

        self.reservation_id = reservation_id
        self.guest = guest
        self.room = room
        self.nights = nights
        self.checked_in = False
        self.checked_out = False
        self.is_cancelled = False
