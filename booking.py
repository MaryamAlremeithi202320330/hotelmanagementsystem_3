"""
Booking Module for Royal Stay Hotel Management System.

This module defines the Booking class and related functionality.
"""

from datetime import datetime, timedelta
import uuid

class Booking:
    """
    Represents a room booking in the hotel.
    
    Attributes:
        _booking_id (str): Unique identifier for the booking.
        _guest (Guest): Reference to the guest making the booking.
        _rooms (list): List of rooms included in the booking.
        _check_in_date (datetime): Check-in date and time.
        _check_out_date (datetime): Check-out date and time.
        _total_cost (float): Total cost of the booking.
        _is_confirmed (bool): Confirmation status of the booking.
        _is_canceled (bool): Cancellation status of the booking.
    """
    
    def __init__(self, guest, check_in_date, check_out_date):
        """
        Initialize a new Booking instance.
        
        Args:
            guest (Guest): Reference to the guest making the booking.
            check_in_date (datetime): Check-in date and time.
            check_out_date (datetime): Check-out date and time.
        """
        self._booking_id = str(uuid.uuid4())[:8]  # Generate a unique booking ID
        self._guest = guest
        self._rooms = []
        self._check_in_date = check_in_date
        self._check_out_date = check_out_date
        self._total_cost = 0.0
        self._is_confirmed = False
        self._is_canceled = False
    
    def add_room(self, room):
        """
        Add a room to the booking.
        
        Args:
            room (Room): The room to add to the booking.
            
        Returns:
            bool: True if the room was successfully added.
            
        Raises:
            ValueError: If the room is not available for the booking dates.
        """
        # Check if the room is available for the booking dates
        if not room.check_availability(self._check_in_date, self._check_out_date):
            raise ValueError(f"Room {room.room_number} is not available for the requested dates")
        
        # Add booking to the room
        room.add_booking(self._check_in_date, self._check_out_date)
        
        self._rooms.append(room)
        self._update_total_cost()
        
        print(f"Room {room.room_number} added to booking {self._booking_id}")
        return True
    
    def remove_room(self, room):
        """
        Remove a room from the booking.
        
        Args:
            room (Room): The room to remove from the booking.
            
        Returns:
            bool: True if the room was successfully removed.
        """
        if room in self._rooms:
            self._rooms.remove(room)
            self._update_total_cost()
            print(f"Room {room.room_number} removed from booking {self._booking_id}")
            return True
        else:
            print(f"Room {room.room_number} is not part of booking {self._booking_id}")
            return False
    
    def _update_total_cost(self):
        """
        Update the total cost of the booking based on rooms and duration.
        """
        # Calculate the number of nights
        nights = (self._check_out_date - self._check_in_date).days
        
        # Calculate the total cost
        self._total_cost = sum(room.price_per_night * nights for room in self._rooms)
    
    def create_booking(self):
        """
        Confirm and create the booking.
        
        Returns:
            bool: True if the booking was successfully created.
        """
        if not self._rooms:
            raise ValueError("Cannot create a booking with no rooms")
        
        self._is_confirmed = True
        
        # Add the booking to the guest's reservations
        self._guest.add_reservation(self)
        
        print(f"Booking {self._booking_id} created successfully for {self._guest.name}")
        return True
    
    def cancel_booking(self):
        """
        Cancel the booking.
        
        Returns:
            bool: True if the booking was successfully canceled.
        """
        if self._is_canceled:
            print(f"Booking {self._booking_id} is already canceled")
            return False
        
        self._is_canceled = True
        self._is_confirmed = False
        
        print(f"Booking {self._booking_id} has been canceled")
        return True
    
    def send_confirmation(self):
        """
        Send a booking confirmation notification.
        
        Returns:
            bool: True if the confirmation was sent successfully.
        """
        if not self._is_confirmed:
            raise ValueError("Cannot send confirmation for an unconfirmed booking")
        
        # In a real system, this would send an email or notification
        print(f"Confirmation for booking {self._booking_id} sent to {self._guest.email}")
        
        # Print booking details
        print(f"Booking Details:")
        print(f"Guest: {self._guest.name}")
        print(f"Check-in: {self._check_in_date.strftime('%Y-%m-%d')}")
        print(f"Check-out: {self._check_out_date.strftime('%Y-%m-%d')}")
        print(f"Rooms: {len(self._rooms)}")
        print(f"Total Cost: ${self._total_cost:.2f}")
        
        return True
    
    def calculate_total(self):
        """
        Calculate the total cost of the booking.
        
        Returns:
            float: Total cost of the booking.
        """
        self._update_total_cost()
        return self._total_cost
    
    # Getter methods
    @property
    def booking_id(self):
        """Get the booking ID."""
        return self._booking_id
    
    @property
    def guest(self):
        """Get the guest."""
        return self._guest
    
    @property
    def rooms(self):
        """Get the list of rooms."""
        return self._rooms
    
    @property
    def check_in_date(self):
        """Get the check-in date."""
        return self._check_in_date
    
    @property
    def check_out_date(self):
        """Get the check-out date."""
        return self._check_out_date
    
    @property
    def total_cost(self):
        """Get the total cost."""
        return self._total_cost
    
    @property
    def is_confirmed(self):
        """Check if the booking is confirmed."""
        return self._is_confirmed
    
    @property
    def is_canceled(self):
        """Check if the booking is canceled."""
        return self._is_canceled
    
    def __str__(self):
        """
        Return a string representation of the Booking object.
        
        Returns:
            str: String representation of the Booking.
        """
        status = "Confirmed" if self._is_confirmed else "Pending"
        if self._is_canceled:
            status = "Canceled"
        
        return f"Booking ID: {self._booking_id}, Guest: {self._guest.name}, " \
               f"Check-in: {self._check_in_date.strftime('%Y-%m-%d')}, " \
               f"Check-out: {self._check_out_date.strftime('%Y-%m-%d')}, " \
               f"Rooms: {len(self._rooms)}, Total: ${self._total_cost:.2f}, Status: {status}"
