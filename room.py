"""
Room Module for Royal Stay Hotel Management System.

This module defines the Room class, RoomType enumeration, and related functionality.
"""

from enum import Enum
from datetime import datetime

class RoomType(Enum):
    """Enumeration of room types available at the hotel."""
    SINGLE = "Single Room"
    DOUBLE = "Double Room"
    SUITE = "Suite"
    DELUXE = "Deluxe Room"

class Room:
    """
    Represents a hotel room with its properties and functionality.
    
    Attributes:
        _room_number (int): Unique room number.
        _room_type (RoomType): Type of room.
        _amenities (list): List of amenities available in the room.
        _price_per_night (float): Cost per night.
        _is_available (bool): Availability status.
        _bookings (list): List of booking periods for the room.
    """
    
    def __init__(self, room_number, room_type, amenities, price_per_night):
        """
        Initialize a new Room instance.
        
        Args:
            room_number (int): Unique room number.
            room_type (RoomType): Type of room.
            amenities (list): List of amenities available in the room.
            price_per_night (float): Cost per night.
        """
        self._room_number = room_number
        self._room_type = room_type
        self._amenities = amenities
        self._price_per_night = price_per_night
        self._is_available = True
        self._bookings = []  # List of (check_in, check_out) tuples
    
    def check_availability(self, check_in_date, check_out_date):
        """
        Check if the room is available for the given dates.
        
        Args:
            check_in_date (datetime): Check-in date.
            check_out_date (datetime): Check-out date.
            
        Returns:
            bool: True if the room is available, False otherwise.
        """
        if check_in_date >= check_out_date:
            raise ValueError("Check-in date must be before check-out date")
        
        for booking_check_in, booking_check_out in self._bookings:
            # Check if there's an overlap with existing bookings
            if (check_in_date < booking_check_out and check_out_date > booking_check_in):
                return False
        
        return True
    
    def add_booking(self, check_in_date, check_out_date):
        """
        Add a booking for this room.
        
        Args:
            check_in_date (datetime): Check-in date.
            check_out_date (datetime): Check-out date.
            
        Returns:
            bool: True if booking was successfully added.
            
        Raises:
            ValueError: If the room is not available for the requested dates.
        """
        if not self.check_availability(check_in_date, check_out_date):
            raise ValueError(f"Room {self._room_number} is not available for the requested dates")
        
        self._bookings.append((check_in_date, check_out_date))
        print(f"Booking added for Room {self._room_number} from {check_in_date.date()} to {check_out_date.date()}")
        return True
    
    def update_status(self, is_available):
        """
        Update the availability status of the room.
        
        Args:
            is_available (bool): New availability status.
        """
        self._is_available = is_available
        status = "available" if is_available else "unavailable"
        print(f"Room {self._room_number} is now {status}")
    
    def get_details(self):
        """
        Get detailed information about the room.
        
        Returns:
            dict: Dictionary containing room details.
        """
        details = {
            "room_number": self._room_number,
            "room_type": self._room_type.value,
            "amenities": self._amenities,
            "price_per_night": self._price_per_night,
            "is_available": self._is_available
        }
        return details
    
    # Getter and setter methods
    @property
    def room_number(self):
        """Get the room number."""
        return self._room_number
    
    @property
    def room_type(self):
        """Get the room type."""
        return self._room_type
    
    @property
    def amenities(self):
        """Get the room amenities."""
        return self._amenities
    
    @amenities.setter
    def amenities(self, value):
        """Set the room amenities."""
        self._amenities = value
    
    @property
    def price_per_night(self):
        """Get the price per night."""
        return self._price_per_night
    
    @price_per_night.setter
    def price_per_night(self, value):
        """Set the price per night."""
        if value < 0:
            raise ValueError("Price cannot be negative")
        self._price_per_night = value
    
    @property
    def is_available(self):
        """Get the availability status."""
        return self._is_available
    
    def __str__(self):
        """
        Return a string representation of the Room object.
        
        Returns:
            str: String representation of the Room.
        """
        amenities_str = ", ".join(self._amenities)
        status = "Available" if self._is_available else "Not Available"
        return f"Room {self._room_number} ({self._room_type.value}) - ${self._price_per_night:.2f} per night - " \
               f"Amenities: {amenities_str} - Status: {status}"