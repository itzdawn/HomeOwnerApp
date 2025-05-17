from app.Entities.service import Service

class UpdateServiceController:
    def updateService(self, serviceId, userId, categoryId, name=None, description=None, price=None):
        service = Service(
                id=serviceId,
                userId=userId,
                name=name,
                description=description,
                categoryId=categoryId, 
                price=price
            )
        return service.updateService(name=name, description=description, price=price)
            
