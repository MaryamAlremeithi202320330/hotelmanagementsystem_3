"""
Guest Module for Royal Stay Hotel Management System.

This module defines the Guest class and related functionality.
"""

class Guest:
    """
    Represents a hotel guest with personal details and account functionality.
    
    Attributes:
        _guest_id (int): Unique identifier for the guest.
        _name (str): Full name of the guest.
        _contact (str): Contact information (phone or email).
        _email (str): Email address of the guest.
        _loyalty_program (LoyaltyProgram): Reference to the guest's loyalty program.
        _reservations (list): List of the guest's reservations.
    """
    
    def __init__(self, guest_id, name, contact, email):
        """
        Initialize a new Guest instance.
        
        Args:
            guest_id (int): Unique identifier for the guest.
            name (str): Full name of the guest.
            contact (str): Contact information (phone).
            email (str): Email address of the guest.
        """
        self._guest_id = guest_id
        self._name = name
        self._contact = contact
        self._email = email
        self._loyalty_program = None
        self._reservations = []
    
    def create_account(self):
        """
        Create a new guest account.
        
        Returns:
            bool: True if account creation was successful, False otherwise.
        """
        print(f"Account created for {self._name}")
        # Logic for account creation would go here
        return True
    
    def update_profile(self, name=None, contact=None, email=None):
        """
        Update the guest's profile information.
        
        Args:
            name (str, optional): New name for the guest.
            contact (str, optional): New contact information.
            email (str, optional): New email address.
            
        Returns:
            bool: True if update was successful, False otherwise.
        """
        if name:
            self._name = name
        if contact:
            self._contact = contact
        if email:
            self._email = email
        
        print(f"Profile updated for {self._name}")
        return True
    
    def view_reservations(self):
        """
        View all reservations made by the guest.
        
        Returns:
            list: List of reservations.
        """
        if not self._reservations:
            print("No reservations found.")
        else:
            print(f"Found {len(self._reservations)} reservations for {self._name}:")
            for reservation in self._reservations:
                print(reservation)
        
        return self._reservations
    
    def add_reservation(self, reservation):
        """
        Add a reservation to the guest's account.
        
        Args:
            reservation (Booking): The reservation to add.
            
        Returns:
            bool: True if the reservation was added successfully.
        """
        self._reservations.append(reservation)
        print(f"Reservation {reservation.booking_id} added to {self._name}'s account.")
        return True
    
    def set_loyalty_program(self, loyalty_program):
        """
        Associate a loyalty program with the guest.
        
        Args:
            loyalty_program (LoyaltyProgram): The loyalty program to associate.
        """
        self._loyalty_program = loyalty_program
    
    def get_loyalty_program(self):
        """
        Get the guest's loyalty program.
        
        Returns:
            LoyaltyProgram: The guest's loyalty program.
        """
        return self._loyalty_program
    
    # Getter and setter methods
    @property
    def guest_id(self):
        """Get the guest ID."""
        return self._guest_id
    
    @property
    def name(self):
        """Get the guest's name."""
        return self._name
    
    @name.setter
    def name(self, value):
        """Set the guest's name."""
        self._name = value
    
    @property
    def contact(self):
        """Get the guest's contact information."""
        return self._contact
    
    @contact.setter
    def contact(self, value):
        """Set the guest's contact information."""
        self._contact = value
    
    @property
    def email(self):
        """Get the guest's email address."""
        return self._email
    
    @email.setter
    def email(self, value):
        """Set the guest's email address."""
        self._email = value
    
    def __str__(self):
        """
        Return a string representation of the Guest object.
        
        Returns:
            str: String representation of the Guest.
        """
        return f"Guest ID: {self._guest_id}, Name: {self._name}, Contact: {self._contact}, Email: {self._email}"
