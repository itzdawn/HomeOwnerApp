from app.Entities.completedService import CompletedService

class SearchServiceHistoryController:
    def searchCompletedServices(self, homeownerId=None, startDate=None, endDate=None, categoryId=None, name=None):
        try:
            return CompletedService.searchCompletedServices(
                homeownerId, startDate, endDate, categoryId, name
            )
        except Exception as e:
            print(f"[SearchServiceHistoryController] Error: {e}")
            return {"success": False, "message": f"Error: {str(e)}"}

    def getAllCompletedServices(self, homeownerId):
        try:
            return CompletedService.getAllCompletedServices(homeownerId)
        except Exception as e:
            print(f"[SearchServiceHistoryController] Error: {e}")
            return {"success": False, "message": f"Error: {str(e)}"}