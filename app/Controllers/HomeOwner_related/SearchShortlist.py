from app.Entities.shortlist import Shortlist

class SearchShortlisthController:
    
    def searchShortlistedServices(self, homeownerId, serviceName=None, categoryId=None):
        try:
            services = Shortlist.searchShortlistedServices(
                homeownerId=homeownerId,
                serviceName=serviceName,
                categoryId=categoryId
            )
            return services
        except Exception as e:
            print(f"[SearchShortlistedServices] Error: {e}")
            return []

    def getShortlists(self, homeownerId):
        try:
            services = Shortlist.getShortlists(homeownerId=homeownerId)
            return services
        except Exception as e:
            print(f"[GetShortlists] Error: {e}")
            return []