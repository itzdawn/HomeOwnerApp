from app.Entities.completedService import CompletedService

class SearchPastServiceController:
    def searchPastServices(self, cleanerId, startDate=None, endDate=None, category=None):
        try:
            completedService = CompletedService()
            return completedService.searchPastServices(cleanerId, startDate, endDate, category)
        except Exception as e:
            print(f"[SearchPastServiceController] Error: {e}")
            return []
            
    def getPastServiceById(self, serviceId, cleanerId):
        """
        Get a single completed service by its ID, ensuring it belongs to the specified cleaner
        
        Args:
            serviceId (int): ID of the completed service to retrieve
            cleanerId (int): ID of the cleaner who should own this service
            
        Returns:
            dict: Service details or None if not found/not authorized
        """
        try:
            completedService = CompletedService()
            return completedService.getPastServiceById(serviceId, cleanerId)
        except Exception as e:
            print(f"[SearchPastServiceController] Error getting past service by ID: {e}")
            return None