from app.Entities.service import Service

class DeleteServiceController:
    def __init__(self):
        pass
        
    def deleteService(self, serviceId, userId):
        try:
            # Check if service exists and belongs to this cleaner
            service = Service.getServiceByServiceId(serviceId)
            if not service:
                return {"success": False, "message": "Service not found"}
                
            # Check if the service belongs to the cleaner
            if service.getUserId() != userId:
                return {"success": False, "message": "You are not authorized to delete this service"}

            response = Service.deleteService(serviceId, userId)
            
            if response:
                return {"success": True, "message": "Service deleted successfully"}
            else:
                return {"success": False, "message": "Failed to delete service"}
                
        except Exception as e:
            print(f"Error deleting service: {str(e)}")
            return {"success": False, "message": f"Error: {str(e)}"}