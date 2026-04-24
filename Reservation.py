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
def total(self):
        return self.room.calculate_price(self.nights)

    def check_in(self):
        if self.is_cancelled:
            raise ValueError("Cannot check in cancelled reservation.")
        if self.checked_in:
            raise ValueError("Guest already checked in.")
        if self.checked_out:
            raise ValueError("Guest already checked out.")
        self.room.book()
        self.checked_in = True

    def check_out(self):
        if self.is_cancelled:
            raise ValueError("Cannot check out cancelled reservation.")
        if not self.checked_in:
            raise ValueError("Guest has not checked in yet.")
        if self.checked_out:
            raise ValueError("Guest already checked out.")
        self.room.release()
        self.checked_out = True

    def cancel(self):
        if self.checked_out:
            raise ValueError("Cannot cancel checked-out reservation.")
        if self.is_cancelled:
            raise ValueError("Reservation already cancelled.")
        if self.checked_in and not self.checked_out:
            self.room.release()
        self.is_cancelled = True

    def status(self):
        if self.is_cancelled:
            return "Cancelled"
        if self.checked_out:
            return "Checked-out"
        if self.checked_in:
            return "Checked-in"
        return "Reserved"

    def __str__(self):
        return (
            f"Reservation #{self.reservation_id} | Guest: {self.guest.name} {self.guest.surname} | "
            f"Room: {self.room.number} ({self.room.room_type()}) | Nights: {self.nights} | "
            f"Total: {self.total():.2f} EUR | Status: {self.status()}"
        )
