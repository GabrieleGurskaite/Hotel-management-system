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
