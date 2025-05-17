from app.Entities.service import Service

class ViewServiceController:
    def getServiceByServiceId(self, serviceId):
        try:
            service = Service.getServiceByServiceId(serviceId)
            if service:
                return service.toDict()
            else:
                return None
        except Exception as e:
            print(f"[ViewServiceController] Fetch Error: {e}")
            return None