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
