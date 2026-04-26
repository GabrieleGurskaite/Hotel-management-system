import unittest
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

from hotel_system import Guest, RoomFactory, Hotel


class HotelSystemTests(unittest.TestCase):
    def test_factory_creates_deluxe_room(self):
        room = RoomFactory.create("deluxe", 201, 80)
        self.assertEqual(room.room_type(), "Deluxe")

    def test_standard_room_price(self):
        room = RoomFactory.create("standard", 101, 50)
        self.assertEqual(room.calculate_price(3), 150)

    def test_invalid_guest_phone_raises_error(self):
        with self.assertRaises(ValueError):
            Guest("Jonas", "Jonaitis", "861234567", 1, "jonas@email.com")
            
    def test_reservation_workflow(self):
        hotel = Hotel("Test Hotel")
        hotel.add_room(RoomFactory.create("standard", 101, 50))
        guest = Guest("Jonas", "Jonaitis", "+37061234567", 1, "jonas@email.com")
        hotel.add_guest(guest)

        reservation = hotel.create_reservation(1, 101, 2)

        self.assertFalse(reservation.checked_in)

        hotel.check_in_guest(reservation.reservation_id)
        self.assertTrue(reservation.checked_in)

        hotel.check_out_guest(reservation.reservation_id)
        self.assertTrue(reservation.checked_out)
        
    def test_total_revenue_after_checkout(self):
        hotel = Hotel("Test Hotel")
        hotel.add_room(RoomFactory.create("standard", 101, 50))
        guest = Guest("Jonas", "Jonaitis", "+37061234567", 1, "jonas@email.com")
        hotel.add_guest(guest)

        reservation = hotel.create_reservation(1, 101, 2)
        hotel.check_in_guest(reservation.reservation_id)
        hotel.check_out_guest(reservation.reservation_id)

        self.assertEqual(hotel.total_revenue(), 100)

    def test_invalid_room_type_raises_error(self):
        with self.assertRaises(ValueError):
            RoomFactory.create("vip", 999, 100)

    def test_cancel_reservation(self):
        hotel = Hotel("Test Hotel")
        hotel.add_room(RoomFactory.create("standard", 101, 50))
        guest = Guest("Jonas", "Jonaitis", "+37061234567", 1, "jonas@email.com")
        hotel.add_guest(guest)

        reservation = hotel.create_reservation(1, 101, 2)
        hotel.cancel_reservation(reservation.reservation_id)

        self.assertTrue(reservation.is_cancelled)

    def test_duplicate_guest_id_raises_error(self):
        hotel = Hotel("Test Hotel")
        guest1 = Guest("Jonas", "Jonaitis", "+37061234567", 1, "jonas@email.com")
        guest2 = Guest("Petras", "Petraitis", "+37061234568", 1, "petras@email.com")

        hotel.add_guest(guest1)

        with self.assertRaises(ValueError):
            hotel.add_guest(guest2)

    def test_duplicate_room_number_raises_error(self):
        hotel = Hotel("Test Hotel")
        room1 = RoomFactory.create("standard", 101, 50)
        room2 = RoomFactory.create("deluxe", 101, 80)

        hotel.add_room(room1)

        with self.assertRaises(ValueError):
            hotel.add_room(room2)


if __name__ == "__main__":
    unittest.main()
