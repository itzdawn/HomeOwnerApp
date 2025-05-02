from app.Entities.completedService import CompletedService

class SearchPastServiceController:
    def searchPastServices(self, cleanerId, startDate=None, endDate=None, category=None):
        try:
            completedService = CompletedService()
            return completedService.searchPastServices(cleanerId, startDate, endDate, category)
        except Exception as e:
            print(f"[SearchPastServiceController] Error: {e}")
            return []