from flask import jsonify, session, request
from app.Entities.shortlist import Shortlist

class ShortlistViewerController:
    @staticmethod
    def view_shortlisted_services():
        """View all shortlisted services for the logged-in homeowner."""
        try:
            homeowner_id = session.get('userId')
            if not homeowner_id:
                return jsonify({"error": "User not authenticated"}), 401

            # Fetch all shortlisted services
            shortlisted_services = Shortlist.view_shortlisted_services(homeowner_id)

            return jsonify({
                "shortlisted_services": shortlisted_services,
                "message": "Shortlisted services retrieved successfully."
            }), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    