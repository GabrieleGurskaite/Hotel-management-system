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

        
