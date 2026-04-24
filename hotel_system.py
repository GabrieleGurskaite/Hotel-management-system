import json
import os
import re
from abc import ABC, abstractmethod


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


class Hotel:
    def __init__(self, name):
        if not name.strip():
            raise ValueError("Hotel name cannot be empty.")
        self.name = name.strip()
        self._rooms = []
        self._guests = []
        self._reservations = []

    @property
    def rooms(self):
        return self._rooms

    @property
    def guests(self):
        return self._guests

    @property
    def reservations(self):
        return self._reservations
        
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

    
class FileManager:
    @staticmethod
    def save_data(filename, hotel):
        data = {"rooms": [], "guests": [], "reservations": []}

        for room in hotel.rooms:
            data["rooms"].append({
                "number": room.number,
                "price": room.price,
                "available": room.available,
                "type": room.room_type().lower()
            })

        for guest in hotel.guests:
            data["guests"].append({
                "name": guest.name,
                "surname": guest.surname,
                "phone": guest.phone,
                "guest_id": guest.guest_id,
                "email": guest.email
            })

        for reservation in hotel.reservations:
            data["reservations"].append({
                "reservation_id": reservation.reservation_id,
                "guest_id": reservation.guest.guest_id,
                "room_number": reservation.room.number,
                "nights": reservation.nights,
                "checked_in": reservation.checked_in,
                "checked_out": reservation.checked_out,
                "is_cancelled": reservation.is_cancelled
            })

        with open(filename, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4)
            
    @staticmethod
    def load_data(filename, hotel):
        if not os.path.exists(filename):
            return

        with open(filename, "r", encoding="utf-8") as file:
            data = json.load(file)

        hotel.rooms.clear()
        hotel.guests.clear()
        hotel.reservations.clear()

        for raw_room in data.get("rooms", []):
            room = RoomFactory.create(raw_room["type"], raw_room["number"], raw_room["price"])
            room.available = raw_room["available"]
            hotel.rooms.append(room)

        for raw_guest in data.get("guests", []):
            guest = Guest(
                raw_guest["name"],
                raw_guest["surname"],
                raw_guest["phone"],
                raw_guest["guest_id"],
                raw_guest["email"]
            )
            hotel.guests.append(guest)

        for raw_reservation in data.get("reservations", []):
            guest = hotel.find_guest(raw_reservation["guest_id"])
            room = hotel.find_room(raw_reservation["room_number"])
            if guest and room:
                reservation = Reservation(
                    raw_reservation["reservation_id"],
                    guest,
                    room,
                    raw_reservation["nights"]
                )
                reservation.checked_in = raw_reservation["checked_in"]
                reservation.checked_out = raw_reservation["checked_out"]
                reservation.is_cancelled = raw_reservation["is_cancelled"]
                hotel.reservations.append(reservation)


def add_room_ui(hotel):
    try:
        room_type = input("Enter room type (standard/deluxe/suite): ").strip().lower()
        number = int(input("Room number: "))
        price = float(input("Base price: "))
        room = RoomFactory.create(room_type, number, price)
        hotel.add_room(room)
        print("Room added successfully.")
    except Exception as error:
        print("Error:", error)
        
        
def add_guest_ui(hotel):
    try:
        name = input("Name: ")
        surname = input("Surname: ")
        phone = input("Phone (+370XXXXXXXX): ")
        guest_id = int(input("Guest ID: "))
        email = input("Email: ")
        guest = Guest(name, surname, phone, guest_id, email)
        hotel.add_guest(guest)
        print("Guest added successfully.")
    except Exception as error:
        print("Error:", error)


def create_reservation_ui(hotel):
    try:
        guest_id = int(input("Guest ID: "))
        room_number = int(input("Room number: "))
        nights = int(input("Nights: "))
        reservation = hotel.create_reservation(guest_id, room_number, nights)
        print("Reservation created successfully.")
        print(reservation)
    except Exception as error:
        print("Error:", error)


def cancel_reservation_ui(hotel):
    try:
        reservation_id = int(input("Reservation ID to cancel: "))
        hotel.cancel_reservation(reservation_id)
        print("Reservation cancelled successfully.")
    except Exception as error:
        print("Error:", error)


def check_in_ui(hotel):
    try:
        reservation_id = int(input("Reservation ID for check-in: "))
        hotel.check_in_guest(reservation_id)
        print("Check-in successful.")
    except Exception as error:
        print("Error:", error)


def check_out_ui(hotel):
    try:
        reservation_id = int(input("Reservation ID for check-out: "))
        hotel.check_out_guest(reservation_id)
        print("Check-out successful.")
    except Exception as error:
        print("Error:", error)

    
def show_available_rooms_ui(hotel):
    print("\n=== AVAILABLE ROOMS ===")
    rooms = hotel.get_free_rooms()
    if not rooms:
        print("No available rooms.")
        return
    for room in rooms:
        print(room)


def show_all_rooms_ui(hotel):
    print("\n=== ALL ROOMS ===")
    if not hotel.rooms:
        print("No rooms found.")
        return
    for room in hotel.rooms:
        print(room)


def show_guests_ui(hotel):
    print("\n=== GUESTS ===")
    if not hotel.guests:
        print("No guests found.")
        return
    for guest in hotel.guests:
        print(guest)


def show_reservations_ui(hotel):
    print("\n=== RESERVATIONS ===")
    if not hotel.reservations:
        print("No reservations found.")
        return
    for reservation in hotel.reservations:
        print(reservation)


def show_total_revenue_ui(hotel):
    print(f"\nTotal revenue: {hotel.total_revenue():.2f} EUR")


def main():
    hotel = Hotel("Hotel Management System")
    data_file = "hotel_data.json"

    if os.path.exists(data_file):
        try:
            FileManager.load_data(data_file, hotel)
        except Exception:
            pass

    if not hotel.rooms:
        hotel.add_room(RoomFactory.create("standard", 101, 50))
        hotel.add_room(RoomFactory.create("deluxe", 201, 80))
        hotel.add_room(RoomFactory.create("suite", 301, 120))

    while True:
        print("\n=== HOTEL MANAGEMENT SYSTEM ===")
        print("1. Show all rooms")
        print("2. Show available rooms")
        print("3. Show guests")
        print("4. Show reservations")
        print("5. Add room")
        print("6. Add guest")
        print("7. Create reservation")
        print("8. Check in guest")
        print("9. Check out guest")
        print("10. Cancel reservation")
        print("11. Show total revenue")
        print("12. Save data and exit")

        choice = input("Choose option: ").strip()

        if choice == "1":
            show_all_rooms_ui(hotel)
        elif choice == "2":
            show_available_rooms_ui(hotel)
        elif choice == "3":
            show_guests_ui(hotel)
        elif choice == "4":
            show_reservations_ui(hotel)
        elif choice == "5":
            add_room_ui(hotel)
        elif choice == "6":
            add_guest_ui(hotel)
        elif choice == "7":
            create_reservation_ui(hotel)
        elif choice == "8":
            check_in_ui(hotel)
        elif choice == "9":
            check_out_ui(hotel)
        elif choice == "10":
            cancel_reservation_ui(hotel)
        elif choice == "11":
            show_total_revenue_ui(hotel)
        elif choice == "12":
            FileManager.save_data(data_file, hotel)
            print("Data saved successfully.")
            print("Program finished successfully.")
            break
        else:
            print("Invalid option.")


if __name__ == "__main__":
    main()
        


        
