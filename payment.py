"""
Payment Module for Royal Stay Hotel Management System.

This module defines the Payment class and related functionality.
"""

import uuid
from datetime import datetime

class Payment:
    """
    Represents a payment for a booking.
    
    Attributes:
        _payment_id (str): Unique identifier for the payment.
        _booking (Booking): Reference to the associated booking.
        _amount (float): Amount to be paid.
        _payment_method (str): Method of payment (e.g., credit card, cash).
        _transaction_date (datetime): Date and time of the transaction.
        _is_successful (bool): Status of the payment.
        _payment_details (dict): Additional details about the payment.
    """
    
    PAYMENT_METHODS = ["Credit Card", "Debit Card", "Cash", "Mobile Wallet", "Bank Transfer"]
    
    def __init__(self, booking, amount, payment_method, payment_details=None):
        """
        Initialize a new Payment instance.
        
        Args:
            booking (Booking): Reference to the associated booking.
            amount (float): Amount to be paid.
            payment_method (str): Method of payment.
            payment_details (dict, optional): Additional details about the payment.
        """
        self._payment_id = str(uuid.uuid4())[:8]  # Generate a unique payment ID
        self._booking = booking
        self._amount = amount
        
        if payment_method not in self.PAYMENT_METHODS:
            raise ValueError(f"Invalid payment method. Choose from: {', '.join(self.PAYMENT_METHODS)}")
        
        self._payment_method = payment_method
        self._transaction_date = None
        self._is_successful = False
        self._payment_details = payment_details or {}
    
    def process_payment(self):
        """
        Process the payment transaction.
        
        Returns:
            bool: True if the payment was successful, False otherwise.
        """
        # In a real system, this would integrate with a payment gateway
        print(f"Processing payment of ${self._amount:.2f} via {self._payment_method}")
        
        # Simulate payment processing
        self._is_successful = True
        self._transaction_date = datetime.now()
        
        print(f"Payment successful! Payment ID: {self._payment_id}")
        return True
    
    def generate_invoice(self):
        """
        Generate an invoice for the payment.
        
        Returns:
            Invoice: A new Invoice object.
        """
        from invoice import Invoice
        
        if not self._is_successful:
            raise ValueError("Cannot generate invoice for an unsuccessful payment")
        
        invoice = Invoice(self._payment_id, self._booking, self)
        print(f"Invoice generated for payment {self._payment_id}")
        return invoice
    
    def apply_discount(self, discount_amount):
        """
        Apply a discount to the payment amount.
        
        Args:
            discount_amount (float): Amount to discount.
            
        Returns:
            float: New amount after discount.
        """
        if discount_amount < 0:
            raise ValueError("Discount amount cannot be negative")
        
        if discount_amount > self._amount:
            raise ValueError("Discount amount cannot exceed payment amount")
        
        self._amount -= discount_amount
        print(f"Discount of ${discount_amount:.2f} applied. New amount: ${self._amount:.2f}")
        return self._amount
    
    # Getter and setter methods
    @property
    def payment_id(self):
        """Get the payment ID."""
        return self._payment_id
    
    @property
    def booking(self):
        """Get the associated booking."""
        return self._booking
    
    @property
    def amount(self):
        """Get the payment amount."""
        return self._amount
    
    @property
    def payment_method(self):
        """Get the payment method."""
        return self._payment_method
    
    @property
    def transaction_date(self):
        """Get the transaction date."""
        return self._transaction_date
    
    @property
    def is_successful(self):
        """Check if the payment was successful."""
        return self._is_successful
    
    def __str__(self):
        """
        Return a string representation of the Payment object.
        
        Returns:
            str: String representation of the Payment.
        """
        status = "Successful" if self._is_successful else "Pending"
        transaction_date = self._transaction_date.strftime("%Y-%m-%d %H:%M:%S") if self._transaction_date else "N/A"
        
        return f"Payment ID: {self._payment_id}, Amount: ${self._amount:.2f}, " \
               f"Method: {self._payment_method}, Date: {transaction_date}, Status: {status}"
