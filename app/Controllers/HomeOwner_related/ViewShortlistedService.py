from app.Entities.shortlist import Shortlist

class ShortlistViewerController:
    def getShortlistedServiceDetail(self, serviceId, homeOwnerId):
        try:
            return Shortlist.getShortlistedServiceDetail(serviceId, homeOwnerId)
        except Exception as e:
            print(f"[ViewShortlistedServiceController] Error: {e}")
            return None
    