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
