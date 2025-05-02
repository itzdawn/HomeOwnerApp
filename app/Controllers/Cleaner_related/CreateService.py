from app.Entities.service import Service

class CreateServiceController:
    def createService(self, userId, name, description, category, price):
        try:
            service = Service(
                userId=userId,
                name=name,
                description=description,
                category=category,
                price=price
            )
            service.createService()
            return True
        except Exception as e:
            print(f"[CreateServiceController] Error: {e}")
            return False
    