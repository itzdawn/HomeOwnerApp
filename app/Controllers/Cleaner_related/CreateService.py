from app.Entities.service import Service

class CreateServiceController:
    def createService(self, userId, name, description, categoryId, price):
        service = Service(
            userId=userId,
            name=name,
            description=description,
            categoryId=categoryId,
            price=price
        )   
        return service.createService()
