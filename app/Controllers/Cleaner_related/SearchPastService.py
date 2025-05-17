from app.Entities.completedService import CompletedService

class SearchPastServiceController:
    def searchPastServices(self, cleanerId=None, startDate=None, endDate=None, categoryId=None, completedServiceId=None, name=None):
        try:
            results = CompletedService.searchPastServices(cleanerId, startDate, endDate, categoryId, name)
            #ensure data type is consistent
            if completedServiceId:
                results = [
                    item for item in results
                    if str(item.get("CompletedServiceId", "")) == str(completedServiceId)
                ]

            return results
        except Exception as e:
            print(f"[SearchPastServiceController] Error: {e}")
            return {"success": False, "message": f"Error: {str(e)}"}
                
    def getAllPastServices(self, cleanerId):
        try:
            return CompletedService.getAllPastServices(cleanerId)
        except Exception as e:
            print(f"[SearchPastServiceController] Error: {e}")
            return {"success": False, "message": f"Error: {str(e)}"}
        

