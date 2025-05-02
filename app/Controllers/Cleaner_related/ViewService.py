from app.Entities.service import Service

class ViewServiceController:
    def getServiceByUserId(self, userId):
        try:
            return Service.getServiceByUserId(userId)
        except Exception as e:
            print(f"[ViewServiceController] Error: {e}")
            return None