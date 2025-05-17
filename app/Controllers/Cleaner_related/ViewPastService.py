from app.Entities.completedService import CompletedService

class ViewPastServiceController:
    def __init__(self):
        pass
    
    def getPastServiceById(self, serviceId):
        try:
            result = CompletedService.getPastServiceById(serviceId)
            if result:
                result.pop("cleaner_name", None)
            return result  #because entity method is used for both cleaner and homeowner.
        except Exception as e:
            print(f"[SearchPastServiceController] Error in getPastServiceById: {e}")
            return None
