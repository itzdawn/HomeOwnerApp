from app.Entities.service import Service

class CreateServiceController:
    def createService(self, userId, name, description, categoryId, price):
        try:
            service = Service(
                userId=userId,
                name=name,
                description=description,
                categoryId=categoryId,
                price=price
            )
            response = service.createService()
            if response:
                return {"message": f"Service: {name} created successfully", "success": True}
            else:
                return {"message": f"Unable to create Service: {name}", "success": False}
        except Exception as e:
            print(f"[CreateServiceController] Error: {e}")
            return {"success": False, "message": f"Error: {str(e)}"}
    