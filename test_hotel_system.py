"""
Test Module for Royal Stay Hotel Management System.

This module tests all the components of the hotel management system.
"""

import sys
from datetime import datetime, timedelta
import unittest

# Import the modules
from guest import Guest
from loyalty_program import LoyaltyProgram
from room import Room, RoomType
from booking import Booking
from payment import Payment
from invoice import Invoice
from guest_service import GuestService, ServiceType
from feedback import Feedback

class TestHotelSystem(unittest.TestCase):
    """
    Test cases for the Royal Stay Hotel Management System.
    """
    
    def setUp(self):
        """Set up test fixtures."""
        # Create guests
        self.guest1 = Guest(1, "John Smith", "+1-555-123-4567", "john.smith@email.com")
        self.guest2 = Guest(2, "Jane Doe", "+1-555-987-6543", "jane.doe@email.com")
        
        # Create loyalty programs
        self.loyalty1 = LoyaltyProgram(101, self.guest1)
        self.guest1.set_loyalty_program(self.loyalty1)
        
        self.loyalty2 = LoyaltyProgram(102, self.guest2)
        self.guest2.set_loyalty_program(self.loyalty2)
        
        # Create rooms
        self.room1 = Room(101, RoomType.SINGLE, ["Wi-Fi", "TV", "Air Conditioning"], 100.0)
        self.room2 = Room(201, RoomType.DOUBLE, ["Wi-Fi", "TV", "Mini-bar", "Air Conditioning"], 150.0)
        self.room3 = Room(301, RoomType.SUITE, ["Wi-Fi", "TV", "Mini-bar", "Air Conditioning", "Jacuzzi"], 250.0)
        
        # Set dates
        self.today = datetime.now()
        self.check_in_date = self.today + timedelta(days=5)
        self.check_out_date = self.today + timedelta(days=8)
    
    def test_guest_account_creation(self):
        """Test the process of guest account creation."""
        print("\n=== Test: Guest Account Creation ===")
        
        # Test case 1: Create a new guest account
        print("Test Case 1: Create a new guest account")
        guest3 = Guest(3, "Bob Johnson", "+1-555-111-2222", "bob.johnson@email.com")
        self.assertTrue(guest3.create_account())
        print(guest3)
        
        # Test case 2: Update guest profile
        print("\nTest Case 2: Update guest profile")
        self.assertTrue(guest3.update_profile(contact="+1-555-333-4444", email="bob.j@email.com"))
        print(guest3)
        
        # Assertions
        self.assertEqual(guest3.name, "Bob Johnson")
        self.assertEqual(guest3.contact, "+1-555-333-4444")
        self.assertEqual(guest3.email, "bob.j@email.com")
    
    def test_searching_available_rooms(self):
        """Test the functionality to search for available rooms."""
        print("\n=== Test: Searching for Available Rooms ===")
        
        # Test case 1: Check availability when room is free
        print("Test Case 1: Check availability when room is free")
        availability1 = self.room1.check_availability(self.check_in_date, self.check_out_date)
        self.assertTrue(availability1)
        print(f"Room {self.room1.room_number} is available: {availability1}")
        
        # Add a booking to room2
        self.room2.add_booking(self.check_in_date, self.check_out_date)
        
        # Test case 2: Check availability when room is booked
        print("\nTest Case 2: Check availability when room is booked")
        availability2 = self.room2.check_availability(self.check_in_date, self.check_out_date)
        self.assertFalse(availability2)
        print(f"Room {self.room2.room_number} is available: {availability2}")
        
        # Test case 3: Filter available rooms based on criteria
        print("\nTest Case 3: Filter available rooms based on criteria")
        all_rooms = [self.room1, self.room2, self.room3]
        available_rooms = [room for room in all_rooms 
                          if room.check_availability(self.check_in_date, self.check_out_date) 
                          and room.price_per_night <= 200.0]
        
        print("Available rooms under $200:")
        for room in available_rooms:
            print(room)
        
        self.assertEqual(len(available_rooms), 1)
        self.assertEqual(available_rooms[0].room_number, self.room1.room_number)
    
    def test_making_room_reservation(self):
        """Test the process of making a room reservation."""
        print("\n=== Test: Making a Room Reservation ===")
        
        # Test case 1: Create a booking with a single room
        print("Test Case 1: Create a booking with a single room")
        booking1 = Booking(self.guest1, self.check_in_date, self.check_out_date)
        booking1.add_room(self.room1)
        booking1.create_booking()
        
        self.assertEqual(len(booking1.rooms), 1)
        self.assertEqual(booking1.guest.name, "John Smith")
        
        # Test case 2: Create a booking with multiple rooms
        print("\nTest Case 2: Create a booking with multiple rooms")
        check_in_date2 = self.today + timedelta(days=15)
        check_out_date2 = self.today + timedelta(days=20)
        
        booking2 = Booking(self.guest2, check_in_date2, check_out_date2)
        booking2.add_room(self.room2)
        booking2.add_room(self.room3)
        booking2.create_booking()
        
        self.assertEqual(len(booking2.rooms), 2)
        self.assertEqual(booking2.total_cost, 5 * (150.0 + 250.0))  # 5 nights * (room2 + room3)
        
        print(booking2)
    
    def test_booking_confirmation_notification(self):
        """Test the booking confirmation notification system."""
        print("\n=== Test: Booking Confirmation Notification ===")
        
        # Test case 1: Send confirmation for a new booking
        print("Test Case 1: Send confirmation for a new booking")
        booking = Booking(self.guest1, self.check_in_date, self.check_out_date)
        booking.add_room(self.room3)
        booking.create_booking()
        self.assertTrue(booking.send_confirmation())
        
        # Test case 2: Attempt to send confirmation for an unconfirmed booking
        print("\nTest Case 2: Attempt to send confirmation for an unconfirmed booking")
        booking2 = Booking(self.guest2, self.check_in_date, self.check_out_date)
        booking2.add_room(self.room1)
        
        try:
            booking2.send_confirmation()
            self.fail("Expected ValueError not raised")
        except ValueError as e:
            print(f"Caught expected exception: {e}")
    
    def test_invoice_generation(self):
        """Test the generation of invoices for bookings."""
        print("\n=== Test: Invoice Generation for a Booking ===")
        
        # Test case 1: Generate invoice for a simple booking
        print("Test Case 1: Generate invoice for a simple booking")
        booking = Booking(self.guest1, self.check_in_date, self.check_out_date)
        booking.add_room(self.room1)
        booking.create_booking()
        
        payment = Payment(booking, booking.total_cost, "Credit Card", 
                         {"card_number": "XXXX-XXXX-XXXX-1234", "expiry": "12/25"})
        payment.process_payment()
        
        invoice = payment.generate_invoice()
        print(invoice)
        
        self.assertEqual(invoice.calculate_total(), booking.total_cost)
        
        # Test case 2: Generate invoice with additional items
        print("\nTest Case 2: Generate invoice with additional items")
        booking2 = Booking(self.guest2, self.check_in_date, self.check_out_date)
        booking2.add_room(self.room2)
        booking2.create_booking()
        
        payment2 = Payment(booking2, booking2.total_cost, "Debit Card")
        payment2.process_payment()
        
        invoice2 = payment2.generate_invoice()
        invoice2.add_item("Late checkout fee", 50.0)
        invoice2.add_item("Room service - Dinner", 75.0)
        
        print(invoice2)
        
        expected_total = booking2.total_cost + 50.0 + 75.0
        self.assertEqual(invoice2.calculate_total(), expected_total)
    
    def test_payment_processing(self):
        """Test the processing of different payment methods."""
        print("\n=== Test: Processing Different Payment Methods ===")
        
        # Test case 1: Process credit card payment
        print("Test Case 1: Process credit card payment")
        booking1 = Booking(self.guest1, self.check_in_date, self.check_out_date)
        booking1.add_room(self.room1)
        booking1.create_booking()
        
        payment1 = Payment(booking1, booking1.total_cost, "Credit Card",
                          {"card_number": "XXXX-XXXX-XXXX-5678", "expiry": "10/26"})
        self.assertTrue(payment1.process_payment())
        
        # Test case 2: Process mobile wallet payment with discount
        print("\nTest Case 2: Process mobile wallet payment with discount")
        booking2 = Booking(self.guest2, self.check_in_date, self.check_out_date)
        booking2.add_room(self.room3)
        booking2.create_booking()
        
        payment2 = Payment(booking2, booking2.total_cost, "Mobile Wallet")
        discount = 50.0  # $50 discount
        payment2.apply_discount(discount)
        self.assertTrue(payment2.process_payment())
        
        expected_amount = booking2.total_cost - discount
        self.assertEqual(payment2.amount, expected_amount)
    
    def test_reservation_history(self):
        """Test the displaying of reservation history."""
        print("\n=== Test: Displaying Reservation History ===")
        
        # Test case 1: View history when no reservations exist
        print("Test Case 1: View history when no reservations exist")
        reservations1 = self.guest1.view_reservations()
        self.assertEqual(len(reservations1), 0)
        
        # Test case 2: View history after adding reservations
        print("\nTest Case 2: View history after adding reservations")
        booking1 = Booking(self.guest1, self.check_in_date, self.check_out_date)
        booking1.add_room(self.room1)
        booking1.create_booking()
        
        check_in_date2 = self.today + timedelta(days=20)
        check_out_date2 = self.today + timedelta(days=25)
        booking2 = Booking(self.guest1, check_in_date2, check_out_date2)
        booking2.add_room(self.room2)
        booking2.create_booking()
        
        reservations2 = self.guest1.view_reservations()
        self.assertEqual(len(reservations2), 2)
    
    def test_cancellation(self):
        """Test the cancellation of reservations."""
        print("\n=== Test: Cancellation of a Reservation ===")
        
        # Test case 1: Cancel a confirmed booking
        print("Test Case 1: Cancel a confirmed booking")
        booking = Booking(self.guest1, self.check_in_date, self.check_out_date)
        booking.add_room(self.room1)
        booking.create_booking()
        
        self.assertTrue(booking.is_confirmed)
        self.assertFalse(booking.is_canceled)
        
        booking.cancel_booking()
        
        self.assertFalse(booking.is_confirmed)
        self.assertTrue(booking.is_canceled)
        
        # Test case 2: Attempt to cancel an already canceled booking
        print("\nTest Case 2: Attempt to cancel an already canceled booking")
        result = booking.cancel_booking()
        self.assertFalse(result)
    
    def test_loyalty_program(self):
        """Test the loyalty program functionality."""
        print("\n=== Test: Loyalty Program ===")
        
        # Test case 1: Earn points from a stay
        print("Test Case 1: Earn points from a stay")
        initial_points = self.loyalty1.points
        stay_value = 500.0
        earned_points = self.loyalty1.earn_points(stay_value)
        
        self.assertEqual(earned_points, 500)
        self.assertEqual(self.loyalty1.points, initial_points + 500)
        
        # Test case 2: Redeem points for a discount
        print("\nTest Case 2: Redeem points for a discount")
        self.loyalty2.earn_points(2000.0)  # Earn 2000 points
        initial_points = self.loyalty2.points
        points_to_redeem = 1000
        
        redemption_value = self.loyalty2.redeem_points(points_to_redeem)
        self.assertEqual(redemption_value, 100.0)  # 1000 points = $100
        self.assertEqual(self.loyalty2.points, initial_points - points_to_redeem)

    def test_guest_services(self):
        """Test guest service requests."""
        print("\n=== Test: Guest Service Requests ===")
        
        # Test case 1: Create a housekeeping request
        print("Test Case 1: Create a housekeeping request")
        service1 = GuestService(self.guest1, 101, ServiceType.HOUSEKEEPING, "Need extra towels")
        self.assertTrue(service1.request_service())
        
        # Test case 2: Track service status
        print("\nTest Case 2: Track service status and assign staff")
        service1.assign_staff("Maria Garcia")
        self.assertEqual(service1.status.value, "Assigned")
        self.assertEqual(service1.assigned_staff, "Maria Garcia")
        
        
        service1.complete_service()
        self.assertEqual(service1.status.value, "Completed")

    def test_feedback_submission(self):
        """Test feedback submission."""
        print("\n=== Test: Feedback Submission ===")
        
        # Create a booking for feedback
        booking = Booking(self.guest1, self.check_in_date, self.check_out_date)
        booking.add_room(self.room1)
        booking.create_booking()
        
        # Test case 1: Submit basic feedback
        print("Test Case 1: Submit basic feedback")
        feedback1 = Feedback(self.guest1, booking, 4, "Great stay, very comfortable room!")
        self.assertTrue(feedback1.submit_review())
        
        # Test case 2: Submit detailed category ratings
        print("\nTest Case 2: Submit detailed category ratings")
        feedback2 = Feedback(self.guest2, booking, 3, "Good location but room could be cleaner.")
        feedback2.rate_experience(cleanliness=3, comfort=4, staff=5, value=4, location=5)
        
        self.assertEqual(feedback2.rating, 4)  # Average of all category ratings
        self.assertEqual(feedback2.categories["cleanliness"], 3)
        self.assertEqual(feedback2.categories["staff"], 5)


if __name__ == "__main__":
    unittest.main()