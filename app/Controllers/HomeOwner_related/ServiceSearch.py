from flask import request, jsonify
from app.Entities.service import Service

class ServiceSearchController:
    @staticmethod
    def search_service_by_id():
        """Search for a service by its service ID."""
        try:
            # Extract the service ID from the request
            service_id = request.args.get('service_id')
            if not service_id:
                return jsonify({"error": "Service ID is required"}), 400

            # Fetch the service using the Service entity
            service = Service.getServiceByServiceId(service_id)
            if not service:
                return jsonify({"error": "Service not found"}), 404

            # Convert the service object to a dictionary for JSON response
            service_data = {
                "id": service.getId(),
                "userId": service.getUserId(),
                "name": service.name,
                "description": service.description,
                "category": service.category,
                "price": service.price,
                "shortlists": service.shortlists,
                "views": service.views,
                "creationDate": service.creationDate
            }

            return jsonify({
                "service": service_data,
                "message": "Service retrieved successfully."
            }), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500