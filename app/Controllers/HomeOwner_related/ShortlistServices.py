from flask import request, jsonify, session
from app.Entities.shortlist import Shortlist

class ShortlistServicesController:
    @staticmethod
    def add_to_shortlist():
        """Add a service to the shortlist."""
        try:
            homeowner_id = session.get('userId')
            service_id = request.json.get('service_id')

            if not homeowner_id or not service_id:
                return jsonify({"error": "Missing required fields"}), 400

            success = Shortlist.add_to_shortlist(homeowner_id, service_id)
            if success:
                return jsonify({"message": "Service added to shortlist successfully."}), 200
            else:
                return jsonify({"error": "Service could not be added to shortlist. It may already be shortlisted."}), 400
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    @staticmethod
    def remove_from_shortlist():
        """Remove a service from the shortlist."""
        try:
            homeowner_id = session.get('userId')
            service_id = request.json.get('service_id')

            if not homeowner_id or not service_id:
                return jsonify({"error": "Missing required fields"}), 400

            success = Shortlist.remove_from_shortlist(homeowner_id, service_id)
            if success:
                return jsonify({"message": "Service removed from shortlist successfully."}), 200
            else:
                return jsonify({"error": "Service could not be removed from shortlist. It may not exist."}), 400
        except Exception as e:
            return jsonify({"error": str(e)}), 500