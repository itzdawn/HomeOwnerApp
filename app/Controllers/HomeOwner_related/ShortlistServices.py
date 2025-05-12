from flask import jsonify
from app.Entities.shortlist import Shortlist

class ShortlistController:
    def addShortlist(self, homeOwnerId, serviceId):
        try:
            success = Shortlist.addShortlist(homeOwnerId, serviceId)

            if success:
                return {"success": True, "message": "Service shortlisted successfully!"}
            else:
                return {"success": False, "message": "Service already shortlisted or failed to add."}
        except Exception as e:
            print(f"[ShortlistController] Error: {e}")
            return {"success": False, "message": "Unexpected error occurred"}
    
    def removeShortlist(self, homeOwnerId, serviceId):
        try:
            success = Shortlist.removeShortlist(homeOwnerId, serviceId)
            if success:
                return {"success": True, "message": "Service removed from shortlist successfully!"}
            else:
                return {"success": False, "message": "Service not found in shortlist or already removed."}
        except Exception as e:
            print(f"[ShortlistController] Error: {e}")
            return {"success": False, "message": "Unexpected error occurred"}
    