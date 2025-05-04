from flask import jsonify, session, request
from app.Entities.shortlist import Shortlist

class ShortlistSearchController:
    @staticmethod
    def search_shortlisted_services():
        """Search shortlisted services based on keyword."""
        try:
            homeowner_id = session.get('userId')
            if not homeowner_id:
                return jsonify({"error": "User not authenticated"}), 401

            # Extract search keyword from query parameters
            keyword = request.args.get('keyword', '').strip()

            # Fetch shortlisted services based on the keyword
            shortlisted_services = Shortlist.search_shortlisted_services(homeowner_id, keyword)

            return jsonify({
                "shortlisted_services": shortlisted_services,
                "message": "Filtered shortlisted services retrieved successfully."
            }), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500