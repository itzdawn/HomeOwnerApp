from app.Entities.service import Service

class DeleteServiceController:
    def __init__(self):
        pass
        
    def deleteService(self, serviceId, userId):
        """
        Delete a service
        
        Args:
            serviceId (int): ID of the service to delete
            userId (int): ID of the cleaner for authorization
            
        Returns:
            dict: Response with status and message
        """
        try:
            # Check if service exists and belongs to this cleaner
            service = Service.getServiceByServiceId(serviceId)
            if not service:
                return {"success": False, "message": "Service not found"}
                
            # Check if the service belongs to the cleaner
            if service.getUserId() != userId:
                return {"success": False, "message": "You are not authorized to delete this service"}
            
            # Check for dependent records before deleting
            # For example, check if service has any bookings/completed services
            
            # Delete the service
            result = Service.deleteService(serviceId, userId)
            
            if result:
                return {"success": True, "message": "Service deleted successfully"}
            else:
                return {"success": False, "message": "Failed to delete service"}
                
        except Exception as e:
            print(f"Error deleting service: {str(e)}")
            return {"success": False, "message": f"Error: {str(e)}"}
    
    def delete(self, serviceId, userId):
        """
        Delete a service by ID (alias for deleteService)
        
        Args:
            serviceId (int): ID of the service to delete
            userId (int): ID of the cleaner for authorization
            
        Returns:
            bool: True if deletion was successful, False otherwise
        """
        # Call the more detailed method but convert the result to a boolean
        result = self.deleteService(serviceId, userId)
        return result.get("success", False)