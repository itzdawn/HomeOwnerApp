from app.Entities.completedService import CompletedService

class ViewServiceHistoryController:
    
    def getCompletedServiceById(self, serviceId):
        try:
            result = CompletedService.getPastServiceById(serviceId)
            #entity method used by both cleaner and homeowner, hence removing the current user's identity is required.
            if result:
                result.pop("homeowner_name", None)  
            return result
        except Exception as e:
            print(f"[ViewServiceHistoryController] Error in getCompletedServiceById: {e}")
            return None