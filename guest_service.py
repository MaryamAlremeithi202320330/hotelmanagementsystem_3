"""
Guest Service Module for Royal Stay Hotel Management System.

This module defines the GuestService class and related functionality.
"""

import uuid
from datetime import datetime
from enum import Enum

class ServiceType(Enum):
    """Enumeration of service types available at the hotel."""
    HOUSEKEEPING = "Housekeeping"
    ROOM_SERVICE = "Room Service"
    MAINTENANCE = "Maintenance"
    TRANSPORTATION = "Transportation"
    CONCIERGE = "Concierge"
    WAKE_UP_CALL = "Wake-up Call"
    LAUNDRY = "Laundry"

class ServiceStatus(Enum):
    """Enumeration of service request statuses."""
    REQUESTED = "Requested"
    ASSIGNED = "Assigned"
    IN_PROGRESS = "In Progress"
    COMPLETED = "Completed"
    CANCELED = "Canceled"

class GuestService:
    """
    Represents a service request made by a guest.
    
    Attributes:
        _service_id (str): Unique identifier for the service request.
        _guest (Guest): Reference to the guest requesting the service.
        _room_number (int): Room number associated with the request.
        _service_type (ServiceType): Type of service requested.
        _description (str): Description of the service request.
        _request_time (datetime): Time when the request was made.
        _status (ServiceStatus): Current status of the request.
        _assigned_staff (str): Name of staff assigned to the request.
        _completion_time (datetime): Time when the request was completed.
    """
    
    def __init__(self, guest, room_number, service_type, description):
        """
        Initialize a new GuestService instance.
        
        Args:
            guest (Guest): Reference to the guest requesting the service.
            room_number (int): Room number associated with the request.
            service_type (ServiceType): Type of service requested.
            description (str): Description of the service request.
        """
        self._service_id = str(uuid.uuid4())[:8]  # Generate a unique service ID
        self._guest = guest
        self._room_number = room_number
        
        if not isinstance(service_type, ServiceType):
            raise ValueError("Service type must be a valid ServiceType enum value")
        
        self._service_type = service_type
        self._description = description
        self._request_time = datetime.now()
        self._status = ServiceStatus.REQUESTED
        self._assigned_staff = None
        self._completion_time = None
    
    def request_service(self):
        """
        Create a new service request.
        
        Returns:
            bool: True if the service request was created successfully.
        """
        print(f"Service request {self._service_id} created for {self._service_type.value}")
        print(f"Guest: {self._guest.name}, Room: {self._room_number}")
        print(f"Description: {self._description}")
        
        return True
    
    def update_status(self, new_status):
        """
        Update the status of the service request.
        
        Args:
            new_status (ServiceStatus): New status for the request.
            
        Returns:
            bool: True if the status was updated successfully.
        """
        if not isinstance(new_status, ServiceStatus):
            raise ValueError("Status must be a valid ServiceStatus enum value")
        
        old_status = self._status
        self._status = new_status
        
        print(f"Service request {self._service_id} status updated from {old_status.value} to {new_status.value}")
        
        if new_status == ServiceStatus.COMPLETED:
            self._completion_time = datetime.now()
            print(f"Service request completed at {self._completion_time.strftime('%Y-%m-%d %H:%M:%S')}")
        
        return True
    
    def assign_staff(self, staff_name):
        """
        Assign staff to the service request.
        
        Args:
            staff_name (str): Name of staff to assign.
            
        Returns:
            bool: True if staff was assigned successfully.
        """
        self._assigned_staff = staff_name
        self.update_status(ServiceStatus.ASSIGNED)
        
        print(f"Staff member '{staff_name}' assigned to service request {self._service_id}")
        return True
    
    def complete_service(self):
        """
        Mark the service request as completed.
        
        Returns:
            bool: True if the service was marked as completed successfully.
        """
        if self._status == ServiceStatus.COMPLETED:
            print(f"Service request {self._service_id} is already completed")
            return False
        
        return self.update_status(ServiceStatus.COMPLETED)
    
    def cancel_service(self):
        """
        Cancel the service request.
        
        Returns:
            bool: True if the service was canceled successfully.
        """
        if self._status == ServiceStatus.COMPLETED:
            print(f"Cannot cancel a completed service request")
            return False
        
        return self.update_status(ServiceStatus.CANCELED)
    
    # Getter methods
    @property
    def service_id(self):
        """Get the service ID."""
        return self._service_id
    
    @property
    def guest(self):
        """Get the guest."""
        return self._guest
    
    @property
    def room_number(self):
        """Get the room number."""
        return self._room_number
    
    @property
    def service_type(self):
        """Get the service type."""
        return self._service_type
    
    @property
    def description(self):
        """Get the service description."""
        return self._description
    
    @property
    def request_time(self):
        """Get the request time."""
        return self._request_time
    
    @property
    def status(self):
        """Get the current status."""
        return self._status
    
    @property
    def assigned_staff(self):
        """Get the assigned staff."""
        return self._assigned_staff
    
    @property
    def completion_time(self):
        """Get the completion time."""
        return self._completion_time
    
    def __str__(self):
        """
        Return a string representation of the GuestService object.
        
        Returns:
            str: String representation of the GuestService.
        """
        assigned = f"Assigned to: {self._assigned_staff}" if self._assigned_staff else "Not assigned"
        completion = f"Completed at: {self._completion_time.strftime('%Y-%m-%d %H:%M:%S')}" if self._completion_time else "Not completed"
        
        return f"Service ID: {self._service_id}, Type: {self._service_type.value}, " \
               f"Room: {self._room_number}, Status: {self._status.value}, " \
               f"{assigned}, {completion}"