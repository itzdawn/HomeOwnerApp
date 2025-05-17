from app.Entities.service import Service

class SearchAvailServiceController:
    def SearchAvailServices(self, serviceName=None, categoryId=None):
        try:
            services = Service.searchAvailServices(serviceName=serviceName, categoryId=categoryId)
            return [s.toDict() for s in services]
        except Exception as e:
            print(f"[SearchAvailServiceController] Error: {e}")
            return {"success": False, "message": f"Error: {str(e)}"}
    
    def getAllAvailServices(self):
        try:
            services = Service.getAllServices()
            return [s.toDict() for s in services]
        except Exception as e:
            print(f"[SearchAvailServiceController] Error: {e}")
            return {"success": False, "message": f"Error: {str(e)}"}
