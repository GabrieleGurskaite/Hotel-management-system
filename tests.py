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
