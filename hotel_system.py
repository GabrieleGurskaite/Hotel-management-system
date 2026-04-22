class Guest:
    def __init__(self, name, surname, phone, guest_id, email):
        if not name.strip() or not surname.strip():
            raise ValueError("Name and surname cannot be empty.")
        if guest_id <= 0:
            raise ValueError("Guest ID must be positive.")
        if not re.fullmatch(r"\+370\d{8}", phone):
            raise ValueError("Phone must be in format +370XXXXXXXX.")
        if not re.fullmatch(r"[^@]+@[^@]+\.[^@]+", email):
            raise ValueError("Invalid email format.")
            
        self.name = name.strip()
        self.surname = surname.strip()
        self.phone = phone
        self.guest_id = guest_id
        self.email = email.strip()
        
    def __str__(self):
        return (
            f"ID: {self.guest_id} | {self.name} {self.surname} | "
         f"Phone: {self.phone} | Email: {self.email}"
        )


class Room(ABC):
    def __init__(self, number, price):
        if number <= 0:
            raise ValueError("Room number must be positive.")
        if price < 0:
            raise ValueError("Price cannot be negative.")
        self.number = number
        self.price = price
        self.available = True
        
    def book(self):
        if not self.available:
            raise ValueError("Room is not available.")
        self.available = False
        
    def release(self):
        self.available = True

    @abstractmethod
    def calculate_price(self, nights):
        raise NotImplementedError

    @abstractmethod
    def room_type(self):
        raise NotImplementedError

    def __str__(self):
        status = "Available" if self.available else "Occupied"
        return (
            f"Room {self.number} | Type: {self.room_type()} | "
            f"Base price: {self.price:.2f} EUR | Status: {status}"
        )
        
        
class StandardRoom(Room):
    def calculate_price(self, nights):
        return self.price * nights

    def room_type(self):
        return "Standard"
        
        
class DeluxeRoom(Room):
    def calculate_price(self, nights):
        return self.price * 1.3 * nights

    def room_type(self):
        return "Deluxe"
        
        
class SuiteRoom(Room):
    def calculate_price(self, nights):
        return self.price * 1.6 * nights

    def room_type(self):
        return "Suite"
        
        
class RoomFactory:
    @staticmethod
    def create(room_type, number, price):
        room_type = room_type.lower()
        if room_type == "standard":
            return StandardRoom(number, price)
        if room_type == "deluxe":
            return DeluxeRoom(number, price)
        if room_type == "suite":
            return SuiteRoom(number, price)
        raise ValueError("Invalid room type. Use standard, deluxe, or suite.")
        
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

        
