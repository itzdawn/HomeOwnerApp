from app.Entities.service import Service

class ViewAvailServiceController:
    def getAvailServiceByServiceId(self, serviceId):
        try:
            return Service.getAvailServiceByServiceId(serviceId)
        except Exception as e:
            print(f"[ViewAvailServiceController] Error: {e}")
            return None