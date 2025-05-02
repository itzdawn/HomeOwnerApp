from app.Entities.service import Service

class DeleteServiceController:
    def deleteService(self, serviceId, userId):
        try:
            return Service.deleteService(serviceId, userId)
        except Exception as e:
            print(f"[DeleteServiceController] Error: {e}")
            return False