from flask import request, jsonify
from app.Entities.service import Service

class ServiceDetailsController:
    @staticmethod
    def get_available_services():
        """Retrieve a list of available services."""
        try:
            # Extract query parameters for filtering
            keyword = request.args.get('keyword', '').strip()
            category = request.args.get('category', '').strip()
            min_price = request.args.get('min_price')
            max_price = request.args.get('max_price')

            # Validate and convert price filters
            try:
                if min_price:
                    min_price = float(min_price)
                if max_price:
                    max_price = float(max_price)
            except ValueError:
                return jsonify({"error": "Invalid price format"}), 400

            # Fetch available services from the database
            services = Service.search(keyword=keyword, category=category, min_price=min_price, max_price=max_price)

            return jsonify({
                "services": services,
                "message": "Available services retrieved successfully."
            }), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500
