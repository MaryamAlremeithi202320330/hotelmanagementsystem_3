"""
Invoice Module for Royal Stay Hotel Management System.

This module defines the Invoice class and related functionality.
"""

from datetime import datetime

class Invoice:
    """
    Represents an invoice for a booking payment.
    
    Attributes:
        _invoice_id (str): Unique identifier for the invoice.
        _booking (Booking): Reference to the associated booking.
        _payment (Payment): Reference to the associated payment.
        _issue_date (datetime): Date and time when the invoice was issued.
        _due_date (datetime): Due date for the payment.
        _items (list): List of line items in the invoice.
    """
    
    def __init__(self, invoice_id, booking, payment):
        """
        Initialize a new Invoice instance.
        
        Args:
            invoice_id (str): Unique identifier for the invoice.
            booking (Booking): Reference to the associated booking.
            payment (Payment): Reference to the associated payment.
        """
        self._invoice_id = invoice_id
        self._booking = booking
        self._payment = payment
        self._issue_date = datetime.now()
        self._due_date = self._issue_date  # For hotel bookings, payment is typically immediate
        self._items = []
        
        # Add line items based on the booking
        self._generate_line_items()
    
    def _generate_line_items(self):
        """
        Generate line items based on the booking details.
        """
        # Calculate number of nights
        nights = (self._booking.check_out_date - self._booking.check_in_date).days
        
        # Add room charges
        for room in self._booking.rooms:
            room_charge = room.price_per_night * nights
            self._items.append({
                "description": f"Room {room.room_number} ({room.room_type.value}) - {nights} nights",
                "amount": room_charge
            })
    
    def add_item(self, description, amount):
        """
        Add a new line item to the invoice.
        
        Args:
            description (str): Description of the item.
            amount (float): Price of the item.
        """
        self._items.append({
            "description": description,
            "amount": amount
        })
        print(f"Item '{description}' added to invoice {self._invoice_id}")
    
    def calculate_total(self):
        """
        Calculate the total amount for the invoice.
        
        Returns:
            float: Total amount.
        """
        return sum(item["amount"] for item in self._items)
    
    def send_invoice(self):
        """
        Send the invoice to the guest.
        
        Returns:
            bool: True if the invoice was sent successfully.
        """
        # In a real system, this would send an email or notification
        guest_email = self._booking.guest.email
        print(f"Invoice {self._invoice_id} sent to {guest_email}")
        
        return True
    
    def generate_pdf(self):
        """
        Generate a PDF version of the invoice.
        
        Returns:
            str: Path to the generated PDF file.
        """
        # In a real system, this would generate a PDF file
        print(f"PDF invoice generated for Invoice {self._invoice_id}")
        return f"invoice_{self._invoice_id}.pdf"
    
    # Getter methods
    @property
    def invoice_id(self):
        """Get the invoice ID."""
        return self._invoice_id
    
    @property
    def booking(self):
        """Get the associated booking."""
        return self._booking
    
    @property
    def payment(self):
        """Get the associated payment."""
        return self._payment
    
    @property
    def issue_date(self):
        """Get the issue date."""
        return self._issue_date
    
    @property
    def due_date(self):
        """Get the due date."""
        return self._due_date
    
    @property
    def items(self):
        """Get the line items."""
        return self._items
    
    def __str__(self):
        """
        Return a string representation of the Invoice object.
        
        Returns:
            str: String representation of the Invoice.
        """
        total = self.calculate_total()
        
        invoice_str = f"Invoice ID: {self._invoice_id}\n"
        invoice_str += f"Issue Date: {self._issue_date.strftime('%Y-%m-%d')}\n"
        invoice_str += f"Guest: {self._booking.guest.name}\n"
        invoice_str += f"Booking ID: {self._booking.booking_id}\n"
        invoice_str += f"Check-in: {self._booking.check_in_date.strftime('%Y-%m-%d')}\n"
        invoice_str += f"Check-out: {self._booking.check_out_date.strftime('%Y-%m-%d')}\n"
        invoice_str += f"\nItems:\n"
        
        for item in self._items:
            invoice_str += f"- {item['description']}: ${item['amount']:.2f}\n"
        
        invoice_str += f"\nTotal Amount: ${total:.2f}"
        
        return invoice_str
