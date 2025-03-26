"""
Feedback Module for Royal Stay Hotel Management System.

This module defines the Feedback class and related functionality.
"""

import uuid
from datetime import datetime

class Feedback:
    """
    Represents feedback from a guest regarding their stay.
    
    Attributes:
        _feedback_id (str): Unique identifier for the feedback.
        _guest (Guest): Reference to the guest providing the feedback.
        _booking (Booking): Reference to the booking associated with the feedback.
        _rating (int): Numerical rating (1-5) given by the guest.
        _comment (str): Detailed comment provided by the guest.
        _submission_date (datetime): Date and time when the feedback was submitted.
        _categories (dict): Ratings for specific categories.
    """
    
    def __init__(self, guest, booking, rating, comment=""):
        """
        Initialize a new Feedback instance.
        
        Args:
            guest (Guest): Reference to the guest providing the feedback.
            booking (Booking): Reference to the booking associated with the feedback.
            rating (int): Numerical rating (1-5) given by the guest.
            comment (str, optional): Detailed comment provided by the guest.
        """
        self._feedback_id = str(uuid.uuid4())[:8]  # Generate a unique feedback ID
        self._guest = guest
        self._booking = booking
        
        # Validate rating
        if not isinstance(rating, int) or rating < 1 or rating > 5:
            raise ValueError("Rating must be an integer between 1 and 5")
        
        self._rating = rating
        self._comment = comment
        self._submission_date = datetime.now()
        self._categories = {
            "cleanliness": 0,
            "comfort": 0,
            "staff": 0,
            "value": 0,
            "location": 0
        }
    
    def submit_review(self):
        """
        Submit the feedback to the system.
        
        Returns:
            bool: True if the feedback was submitted successfully.
        """
        print(f"Feedback submitted successfully. Feedback ID: {self._feedback_id}")
        print(f"Guest: {self._guest.name}")
        print(f"Booking: {self._booking.booking_id}")
        print(f"Rating: {self._rating}/5")
        if self._comment:
            print(f"Comment: {self._comment}")
        
        return True
    
    def rate_category(self, category, rating):
        """
        Provide a rating for a specific category.
        
        Args:
            category (str): The category to rate.
            rating (int): The rating value (1-5).
            
        Returns:
            bool: True if the category rating was updated successfully.
            
        Raises:
            ValueError: If category is invalid or rating is out of range.
        """
        if category not in self._categories:
            raise ValueError(f"Invalid category. Choose from: {', '.join(self._categories.keys())}")
        
        if not isinstance(rating, int) or rating < 1 or rating > 5:
            raise ValueError("Rating must be an integer between 1 and 5")
        
        self._categories[category] = rating
        print(f"Category '{category}' rated {rating}/5")
        return True
    
    def rate_experience(self, cleanliness, comfort, staff, value, location):
        """
        Rate all categories of the guest experience at once.
        
        Args:
            cleanliness (int): Rating for cleanliness (1-5).
            comfort (int): Rating for comfort (1-5).
            staff (int): Rating for staff service (1-5).
            value (int): Rating for value for money (1-5).
            location (int): Rating for location (1-5).
            
        Returns:
            bool: True if all category ratings were updated successfully.
        """
        self.rate_category("cleanliness", cleanliness)
        self.rate_category("comfort", comfort)
        self.rate_category("staff", staff)
        self.rate_category("value", value)
        self.rate_category("location", location)
        
        # Calculate average rating based on categories
        total_rating = sum(self._categories.values())
        avg_rating = round(total_rating / len(self._categories))
        
        # Update overall rating
        self._rating = avg_rating
        
        print(f"All categories rated. Overall rating: {self._rating}/5")
        return True
    
    @staticmethod
    def view_feedback(booking_id=None, guest_id=None):
        """
        View feedback based on booking or guest.
        
        Args:
            booking_id (str, optional): ID of the booking to view feedback for.
            guest_id (int, optional): ID of the guest to view feedback for.
            
        Returns:
            str: String representation of the feedback.
        """
        # In a real system, this would query a database
        if booking_id:
            print(f"Viewing feedback for booking {booking_id}")
        elif guest_id:
            print(f"Viewing feedback for guest {guest_id}")
        else:
            print("Viewing all feedback")
        
        return "Feedback details would be displayed here"
    
    # Getter methods
    @property
    def feedback_id(self):
        """Get the feedback ID."""
        return self._feedback_id
    
    @property
    def guest(self):
        """Get the guest."""
        return self._guest
    
    @property
    def booking(self):
        """Get the booking."""
        return self._booking
    
    @property
    def rating(self):
        """Get the overall rating."""
        return self._rating
    
    @property
    def comment(self):
        """Get the comment."""
        return self._comment
    
    @comment.setter
    def comment(self, value):
        """Set the comment."""
        self._comment = value
    
    @property
    def submission_date(self):
        """Get the submission date."""
        return self._submission_date
    
    @property
    def categories(self):
        """Get the category ratings."""
        return self._categories
    
    def __str__(self):
        """
        Return a string representation of the Feedback object.
        
        Returns:
            str: String representation of the Feedback.
        """
        categories_str = ", ".join([f"{cat}: {rating}/5" for cat, rating in self._categories.items() if rating > 0])
        categories_info = f", Categories: {categories_str}" if categories_str else ""
        
        return f"Feedback ID: {self._feedback_id}, Guest: {self._guest.name}, " \
               f"Booking: {self._booking.booking_id}, Rating: {self._rating}/5" \
               f"{categories_info}, Date: {self._submission_date.strftime('%Y-%m-%d')}"
