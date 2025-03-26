"""
Loyalty Program Module for Royal Stay Hotel Management System.

This module defines the LoyaltyProgram class and related functionality.
"""

class LoyaltyProgram:
    """
    Represents a loyalty program for hotel guests.
    
    Attributes:
        _member_id (int): Unique identifier for the loyalty program member.
        _points (int): Current point balance.
        _tier (str): Membership tier (e.g., "Silver", "Gold", "Platinum").
        _guest (Guest): Reference to the associated guest.
    """
    
    # Tier thresholds
    TIER_THRESHOLDS = {
        "Bronze": 0,
        "Silver": 1000,
        "Gold": 5000,
        "Platinum": 10000
    }
    
    def __init__(self, member_id, guest):
        """
        Initialize a new LoyaltyProgram instance.
        
        Args:
            member_id (int): Unique identifier for the loyalty program member.
            guest (Guest): Reference to the associated guest.
        """
        self._member_id = member_id
        self._points = 0
        self._tier = "Bronze"
        self._guest = guest
    
    def earn_points(self, stay_value):
        """
        Earn points based on the value of a stay.
        
        Args:
            stay_value (float): The monetary value of the stay.
            
        Returns:
            int: Number of points earned.
        """
        # Calculate points (1 point per $1 spent)
        points_earned = int(stay_value)
        self._points += points_earned
        self._update_tier()
        
        print(f"Earned {points_earned} points. New balance: {self._points} points.")
        return points_earned
    
    def redeem_points(self, points_to_redeem):
        """
        Redeem points for rewards.
        
        Args:
            points_to_redeem (int): Number of points to redeem.
            
        Returns:
            float: The monetary value of the redeemed points.
            
        Raises:
            ValueError: If there are insufficient points.
        """
        if points_to_redeem > self._points:
            raise ValueError("Insufficient points for redemption")
        
        # Calculate value (1 point = $0.10)
        redemption_value = points_to_redeem * 0.10
        self._points -= points_to_redeem
        self._update_tier()
        
        print(f"Redeemed {points_to_redeem} points for ${redemption_value:.2f}. Remaining balance: {self._points} points.")
        return redemption_value
    
    def check_balance(self):
        """
        Check the current point balance.
        
        Returns:
            int: Current point balance.
        """
        print(f"Current point balance: {self._points} points. Tier: {self._tier}")
        return self._points
    
    def _update_tier(self):
        """
        Update the membership tier based on points.
        """
        for tier, threshold in sorted(self.TIER_THRESHOLDS.items(), key=lambda x: x[1], reverse=True):
            if self._points >= threshold:
                if self._tier != tier:
                    self._tier = tier
                    print(f"Congratulations! You have been upgraded to {tier} tier.")
                break
    
    # Getter and setter methods
    @property
    def member_id(self):
        """Get the member ID."""
        return self._member_id
    
    @property
    def points(self):
        """Get the current point balance."""
        return self._points
    
    @property
    def tier(self):
        """Get the membership tier."""
        return self._tier
    
    def __str__(self):
        """
        Return a string representation of the LoyaltyProgram object.
        
        Returns:
            str: String representation of the LoyaltyProgram.
        """
        return f"Loyalty Program - Member ID: {self._member_id}, Points: {self._points}, Tier: {self._tier}"
