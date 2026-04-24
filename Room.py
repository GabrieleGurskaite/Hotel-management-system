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
