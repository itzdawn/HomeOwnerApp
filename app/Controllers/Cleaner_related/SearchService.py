from app.Entities.service import Service

class SearchServiceController:
    def searchServices(self, keyword):
        try:
            return Service.searchServices(keyword)
        except Exception as e:
            print(f"[SearchServiceController] Error: {e}")
            return []