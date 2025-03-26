"""
Main Module for Royal Stay Hotel Management System.

This module provides a simple demo of the Royal Stay Hotel Management System.
"""

from datetime import datetime, timedelta
import sys

# Import the modules
from guest import Guest
from loyalty_program import LoyaltyProgram
from room import Room, RoomType
from booking import Booking
from payment import Payment
from invoice import Invoice
from guest_service import GuestService, ServiceType, ServiceStatus
from feedback import Feedback

def main():
    """
    Main function to demonstrate the hotel management system.
    """
    print("=" * 80)
    print("Welcome to Royal Stay Hotel Management System".center(80))
    print("=" * 80)
    
    # Create some rooms
    print("\nCreating hotel rooms...")
    rooms = [
        Room(101, RoomType.SINGLE, ["Wi-Fi", "TV", "Air Conditioning"], 100.0),
        Room(102, RoomType.SINGLE, ["Wi-Fi", "TV", "Air Conditioning"], 100.0),
        Room(201, RoomType.DOUBLE, ["Wi-Fi", "TV", "Mini-bar", "Air Conditioning"], 150.0),
        Room(202, RoomType.DOUBLE, ["Wi-Fi", "TV", "Mini-bar", "Air Conditioning"], 150.0),
        Room(301, RoomType.SUITE, ["Wi-Fi", "TV", "Mini-bar", "Air Conditioning", "Jacuzzi"], 250.0),
        Room(302, RoomType.SUITE, ["Wi-Fi", "TV", "Mini-bar", "Air Conditioning", "Jacuzzi"], 250.0),
        Room(401, RoomType.DELUXE, ["Wi-Fi", "TV", "Mini-bar", "Air Conditioning", "Jacuzzi", "Balcony", "Kitchen"], 350.0)
    ]
    
    print(f"Created {len(rooms)} rooms:")
    for room in rooms:
        print(f"  - {room}")
    
    # Create some guests
    print("\nCreating guest accounts...")
    guests = [
        Guest(1, "John Smith", "+1-555-123-4567", "john.smith@email.com"),
        Guest(2, "Jane Doe", "+1-555-987-6543", "jane.doe@email.com"),
        Guest(3, "Bob Johnson", "+1-555-456-7890", "bob.johnson@email.com")
    ]
    
    # Create account for each guest
    for guest in guests:
        guest.create_account()
        
    # Set up loyalty programs
    print("\nSetting up loyalty programs...")
    for i, guest in enumerate(guests):
        loyalty = LoyaltyProgram(100 + i, guest)
        guest.set_loyalty_program(loyalty)
        print(f"  - Loyalty program set up for {guest.name}: {loyalty}")
    
    # Give some loyalty points to a guest
    guests[0].get_loyalty_program().earn_points(5000)
    print(f"  - Added 5000 points to {guests[0].name}'s loyalty program")
    guests[0].get_loyalty_program().check_balance()
    
    # Demo the booking process
    print("\n" + "=" * 80)
    print("BOOKING PROCESS DEMO".center(80))
    print("=" * 80)
    
    # Set dates
    today = datetime.now()
    check_in_date = today + timedelta(days=5)
    check_out_date = today + timedelta(days=8)
    
    # 1. Search for available rooms
    print("\n1. Searching for available rooms for dates:")
    print(f"   Check-in: {check_in_date.strftime('%Y-%m-%d')}")
    print(f"   Check-out: {check_out_date.strftime('%Y-%m-%d')}")
    
    available_rooms = [room for room in rooms 
                      if room.check_availability(check_in_date, check_out_date)]
    
    print(f"\nFound {len(available_rooms)} available rooms:")
    for room in available_rooms:
        print(f"  - {room}")
    
    # 2. Create a booking
    guest = guests[0]
    print(f"\n2. Creating a booking for {guest.name}:")
    booking = Booking(guest, check_in_date, check_out_date)
    
    # Add rooms to the booking
    selected_room = rooms[2]  # Select room 201 (DOUBLE)
    booking.add_room(selected_room)
    
    # 3. Confirm the booking
    print("\n3. Confirming the booking:")
    booking.create_booking()
    booking.send_confirmation()
    
    # 4. Process payment
    print("\n4. Processing payment:")
    payment = Payment(booking, booking.total_cost, "Credit Card", 
                    {"card_number": "XXXX-XXXX-XXXX-1234", "expiry": "12/25"})
    payment.process_payment()
    
    # 5. Generate invoice
    print("\n5. Generating invoice:")
    invoice = payment.generate_invoice()
    print(invoice)
    
    # Demo the guest services
    print("\n" + "=" * 80)
    print("GUEST SERVICES DEMO".center(80))
    print("=" * 80)
    
    # Create a service request
    print("\n1. Creating a service request:")
    service = GuestService(guest, selected_room.room_number, ServiceType.HOUSEKEEPING, "Need extra towels and pillows")
    service.request_service()
    
    # Update service status
    print("\n2. Updating service status:")
    service.assign_staff("Maria Garcia")
    service.update_status(ServiceStatus.IN_PROGRESS)
    service.complete_service()
    
    # Demo the feedback process
    print("\n" + "=" * 80)
    print("FEEDBACK PROCESS DEMO".center(80))
    print("=" * 80)
    
    # Submit feedback
    print("\n1. Submitting feedback:")
    feedback = Feedback(guest, booking, 4, "Great stay overall, but the room service was a bit slow.")
    feedback.submit_review()
    
    # Rate categories
    print("\n2. Rating specific categories:")
    feedback.rate_experience(cleanliness=5, comfort=4, staff=4, value=4, location=5)
    
    # Demo the loyalty program redemption
    print("\n" + "=" * 80)
    print("LOYALTY PROGRAM REDEMPTION DEMO".center(80))
    print("=" * 80)
    
    # Check balance
    loyalty = guest.get_loyalty_program()
    print("\n1. Checking loyalty point balance:")
    loyalty.check_balance()
    
    # Redeem points
    print("\n2. Redeeming points:")
    points_to_redeem = 1000
    redemption_value = loyalty.redeem_points(points_to_redeem)
    print(f"Redeemed {points_to_redeem} points for ${redemption_value:.2f}")
    
    # Check new balance
    print("\n3. Checking updated balance:")
    loyalty.check_balance()
    
    # Demo cancellation
    print("\n" + "=" * 80)
    print("BOOKING CANCELLATION DEMO".center(80))
    print("=" * 80)
    
    # Create another booking for cancellation demo
    print("\n1. Creating a new booking:")
    future_check_in = today + timedelta(days=15)
    future_check_out = today + timedelta(days=20)
    
    cancellation_booking = Booking(guests[1], future_check_in, future_check_out)
    cancellation_booking.add_room(rooms[4])  # Suite
    cancellation_booking.create_booking()
    print(cancellation_booking)
    
    # Cancel the booking
    print("\n2. Canceling the booking:")
    cancellation_booking.cancel_booking()
    print(cancellation_booking)
    
    print("\n" + "=" * 80)
    print("ROYAL STAY HOTEL MANAGEMENT SYSTEM DEMO COMPLETE".center(80))
    print("=" * 80)

if __name__ == "__main__":
    main()
