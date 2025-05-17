from app.Entities.service import Service

class SearchServiceController:
    def searchServices(self, userId=None, serviceId=None, serviceName=None, categoryId=None):
        try:
            services = Service.searchServices(userId=userId, serviceId=serviceId, serviceName=serviceName, categoryId=categoryId)
            return [s.toDict() for s in services]
        except Exception as e:
            print(f"[SearchServiceController] Error: {e}")
            return {"success": False, "message": f"Error: {str(e)}"}

    def getAllServiceByUserId(self, userId):
        try:
            services = Service.getAllServiceByUserId(userId)
            return [s.toDict() for s in services]
        except Exception as e:
            print(f"[SearchServiceController] Error: {e}")
            return {"success": False, "message": f"Error: {str(e)}"}