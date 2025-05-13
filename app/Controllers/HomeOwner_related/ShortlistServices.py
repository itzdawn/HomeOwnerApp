from flask import jsonify
from app.Entities.shortlist import Shortlist

class ShortlistController:
    def addShortlist(self, homeOwnerId, serviceId):
        
        return Shortlist.addShortlist(homeOwnerId, serviceId)

    def removeShortlist(self, homeOwnerId, serviceId):
        
        return Shortlist.removeShortlist(homeOwnerId, serviceId)