from app.Entities.completedService import CompletedService

class ViewPastServiceController:
    def __init__(self):
        pass
    
    def getPastServiceById(self, serviceId):
        try:
            return CompletedService.getPastServiceById(serviceId)
        except Exception as e:
            print(f"[SearchPastServiceController] Error in getPastServiceById: {e}")
            return None
