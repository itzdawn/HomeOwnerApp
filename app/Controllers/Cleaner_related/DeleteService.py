from app.Entities.service import Service

class DeleteServiceController:

    def deleteService(self, serviceId, userId):
        service = Service.getServiceByServiceId(serviceId)
        if not service:
            return {"success": False, "message": "Service not found"}
                
        # Check if the service belongs to the cleaner
        if service.getUserId() != userId:
            return {"success": False, "message": "You are not authorized to delete this service"}

        return Service.deleteService(serviceId, userId)     
            