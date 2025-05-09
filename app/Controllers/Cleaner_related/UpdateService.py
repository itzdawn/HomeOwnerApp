from app.Entities.service import Service

class UpdateServiceController:
    def updateService(self, serviceId, userId, name, description, categoryId, price):
        try:
            service = Service(
                id=serviceId,
                userId=userId,
                name=name,
                description=description,
                categoryId=categoryId, 
                price=price
            )
            response = service.updateService()
            if response:
                return {"success": True, "message": "User updated successfully"}
            else:
                return {"success": False, "message": "Failed to update user"}
        except Exception as e:
            print(f"[UpdateServiceController] Error: {e}")
            return {"success": False, "message": f"Error: {str(e)}"}