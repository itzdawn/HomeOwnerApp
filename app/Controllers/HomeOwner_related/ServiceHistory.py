from flask import request, jsonify, session
from app.Entities.completedService import CompletedService

class ServiceHistoryController:
    @staticmethod
    def get_service_history():
        """Fetch service history for the homeowner."""
        try:
            homeowner_id = session.get('userId')
            if not homeowner_id:
                return jsonify({"error": "User not authenticated"}), 401

            # Extract query parameters
            start_date = request.args.get('start_date', '').strip()
            end_date = request.args.get('end_date', '').strip()
            category = request.args.get('category', '').strip()

            # Fetch service history using the CompletedService entity
            service_history = CompletedService.searchPastServices(
                cleanerId=homeowner_id,  # Assuming cleanerId is used for homeowner_id in this context
                startDate=start_date if start_date else None,
                endDate=end_date if end_date else None,
                category=category if category else None
            )

            return jsonify({
                "service_history": service_history,
                "message": "Service history retrieved successfully."
            }), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500