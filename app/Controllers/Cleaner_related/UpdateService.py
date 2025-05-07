from app.Entities.service import Service

class UpdateServiceController:
    def getServiceByServiceId(self, serviceId):
        try:
            return Service.getServiceByServiceId(serviceId)
        except Exception as e:
            print(f"[UpdateServiceController] Fetch Error: {e}")
            return None
    def updateService(self, serviceId, userId, name, description, category, price):
        try:
            service = Service(
                id=serviceId,
                userId=userId,
                name=name,
                description=description,
                category=category, 
                price=price
            )
            service.updateService()
            return True
        except Exception as e:
            print(f"[UpdateServiceController] Error: {e}")
            return False