from app.Entities.completedService import CompletedService as completedService

class SearchPastServiceController:
    def searchPastServices(self, cleanerId, startDate=None, endDate=None, category_id=None, completed_service_id=None):
        """
        Search for past services with optional filters
        
        Args:
            cleanerId (int): ID of the cleaner
            startDate (str, optional): Start date for filtering
            endDate (str, optional): End date for filtering
            category_id (int, optional): Category ID for filtering
            completed_service_id (int, optional): Completed Service ID for filtering
            
        Returns:
            list: List of service dictionaries
        """
        print(f"DEBUG - SearchPastServiceController.searchPastServices: cleanerId={cleanerId}, startDate={startDate}, endDate={endDate}, category_id={category_id}, completed_service_id={completed_service_id}")
        
        # Get initial results based on standard filters
        results = completedService.searchPastServices(cleanerId, startDate, endDate, category_id)
        
        # Additional filtering by completed_service_id if provided
        if completed_service_id:
            filtered_results = []
            for item in results:
                # Convert both to strings for comparison
                if str(item.get('CompletedServiceId', '')) == str(completed_service_id):
                    filtered_results.append(item)
                    print(f"DEBUG - Found matching completed service: {item}")
            return filtered_results
        
        return results

    def getPastServiceById(self, serviceId, cleanerId):
        """
        Get a specific completed service by ID
        
        Args:
            serviceId (int): ID of the completed service
            cleanerId (int): ID of the cleaner for authorization
            
        Returns:
            dict: Service details or None if not found
        """
        # This calls the entity method to get the service details
        return completedService.getPastServiceById(serviceId, cleanerId)