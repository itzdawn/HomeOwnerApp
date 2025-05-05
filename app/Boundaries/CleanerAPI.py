from flask import Blueprint, jsonify, request, session
from app.Controllers.Cleaner_related.CreateService import CreateServiceController
from app.Controllers.Cleaner_related.DeleteService import DeleteServiceController
from app.Controllers.Cleaner_related.UpdateService import UpdateServiceController
from app.Controllers.Cleaner_related.SearchPastService import SearchPastServiceController
from app.Boundaries.Login import login_required

# Blueprint for all cleaner API endpoints
cleaner_api_bp = Blueprint('cleaner_api', __name__)

@cleaner_api_bp.route('/services', methods=['GET'])
@login_required
def get_services_api():
    # Get services for the logged-in cleaner
    userId = session.get('userId')
    print(f"DEBUG - Session contents: {session}")
    print(f"DEBUG - get_services_api, userId: {userId}")
    
    if not userId:
        return jsonify({"error": "User not logged in"}), 401

    # Get search/filter parameters
    service_id = request.args.get('service_id')
    service_name = request.args.get('service_name')
    category = request.args.get('category')
    
    # Get pagination parameters
    page = int(request.args.get('page', 1))
    items_per_page = int(request.args.get('items_per_page', 10))

    # Use enhanced filterServices method for efficient database filtering
    from app.Entities.service import Service
    services = Service.filterServices(
        userId=userId,
        serviceId=service_id,
        serviceName=service_name,
        category=category
    )
    
    if not services:
        # Return empty result in expected format
        return jsonify({"services": [], "total": 0})
    
    # Get total count for pagination
    total_count = len(services)
    
    # Apply pagination manually
    start_idx = (page - 1) * items_per_page
    end_idx = start_idx + items_per_page
    paginated_services = services[start_idx:end_idx]
    
    # Convert to dict for JSON serialization
    services_data = [service.to_dict() for service in paginated_services]
        
    # Return in the format expected by frontend
    return jsonify({
        "services": services_data,
        "total": total_count
    })

@cleaner_api_bp.route('/services/<int:service_id>', methods=['GET'])
@login_required
def get_service_by_id(service_id):
    # Get a single service by ID
    userId = session.get('userId')
    if not userId:
        return jsonify({"error": "User not logged in"}), 401

    controller = UpdateServiceController()
    service = controller.getServiceByServiceId(service_id)
    
    if not service:
        return jsonify({"error": "Service not found"}), 404
    
    if hasattr(service, 'to_dict'):
        service = service.to_dict()
        
    return jsonify(service)

@cleaner_api_bp.route('/services/create', methods=['POST'])
@login_required
def create_service_api():
    # Create a new service
    try:
        userId = session.get('userId')
        if not userId:
            return jsonify({"error": "User not logged in"}), 401

        data = request.get_json()
        if not data:
            return jsonify({"error": "Invalid input"}), 400

        controller = CreateServiceController()
        result = controller.createService(
            userId=userId,
            name=data.get('name'),
            description=data.get('description'),
            category=data.get('category'),
            price=float(data.get('price', 0))
        )
        
        if result:
            # Return success response
            return jsonify({"success": True, "message": "Service created successfully"}), 201
        else:
            return jsonify({"error": "Service creation failed"}), 500
    except Exception as e:
        print(f"Error creating service: {str(e)}")
        return jsonify({"error": "Server error"}), 500

@cleaner_api_bp.route('/services/update/<int:service_id>', methods=['PUT'])
@login_required
def update_service_api(service_id):
    # Update an existing service
    try:
        userId = session.get('userId')
        if not userId:
            return jsonify({"error": "User not logged in"}), 401

        data = request.get_json()
        if not data:
            return jsonify({"error": "Invalid input"}), 400

        controller = UpdateServiceController()
        success = controller.updateService(
            serviceId=service_id,
            userId=userId,
            name=data.get('name'),
            description=data.get('description'),
            category=data.get('category'),
            price=float(data.get('price', 0))
        )

        if success:
            return jsonify({"success": True, "message": "Service updated successfully"})
        else:
            return jsonify({"error": "Update failed or unauthorized"}), 403
    except Exception as e:
        print(f"Error updating service: {str(e)}")
        return jsonify({"error": "Server error"}), 500

@cleaner_api_bp.route('/services/delete/<int:service_id>', methods=['DELETE'])
@login_required
def delete_service_api(service_id):
    # Delete a service
    try:
        userId = session.get('userId')
        if not userId:
            return jsonify({"error": "User not logged in"}), 401

        controller = DeleteServiceController()
        success = controller.delete(service_id, userId)

        if success:
            return jsonify({"success": True, "message": "Service deleted successfully"})
        else:
            return jsonify({"error": "Delete failed or unauthorized"}), 403
    except Exception as e:
        print(f"Error deleting service: {str(e)}")
        return jsonify({"error": "Server error"}), 500

@cleaner_api_bp.route('/service-history', methods=['GET'])
@login_required
def get_service_history_api():
    # Get service history with optional filters
    userId = session.get("userId")
    print(f"DEBUG - Session contents: {session}")
    print(f"DEBUG - get_service_history_api, userId: {userId}")
    
    if not userId:
        return jsonify({"error": "User not logged in"}), 401

    # Get filter parameters from query string
    start_date = request.args.get("start_date")
    end_date = request.args.get("end_date")
    category = request.args.get("category")
    service_id_filter = request.args.get("service_id")
    service_name_filter = request.args.get("service_name")
    
    # Get pagination parameters
    page = int(request.args.get('page', 1))
    items_per_page = int(request.args.get('items_per_page', 10))
    
    # Let the controller handle fetching and potentially filtering
    controller = SearchPastServiceController()
    try:
        results = controller.searchPastServices(userId, start_date, end_date, category)
        
        if not results:
            return jsonify({"services": [], "total": 0})

        # Convert results to dictionaries if they are objects
        if hasattr(results[0], 'to_dict'):
             processed_results = [item.to_dict() for item in results]
        else: # Assuming it might already be list of dicts
             processed_results = results

        # Optional: Apply secondary filters if controller didn't handle them
        filtered_results = []
        if service_id_filter or service_name_filter:
            for item in processed_results:
                 # Check service_id filter
                 if service_id_filter and str(item.get('service_id', '')) != service_id_filter:
                     continue
                 # Check service_name filter (case-insensitive)
                 # Ensure the key matches what the controller/to_dict returns (e.g., 'service_name' or 'name')
                 service_name_in_item = item.get('service_name') or item.get('name')
                 if service_name_filter and (not service_name_in_item or service_name_filter.lower() not in service_name_in_item.lower()):
                     continue
                 filtered_results.append(item)
        else:
             filtered_results = processed_results
                
        # Get total count for pagination
        total_count = len(filtered_results)
        
        # Apply pagination manually
        start_idx = (page - 1) * items_per_page
        end_idx = start_idx + items_per_page
        paginated_results = filtered_results[start_idx:end_idx]
        
        # Return in the format expected by frontend
        return jsonify({
            "services": paginated_results,
            "total": total_count
        })
    except Exception as e:
        # Log the detailed error for debugging
        import traceback
        print(f"Error searching past services: {str(e)}\n{traceback.format_exc()}")
        return jsonify({"error": "Server error processing service history"}), 500 

@cleaner_api_bp.route('/service-history/<int:service_id>', methods=['GET'])
@login_required
def get_service_history_detail(service_id):
    # Get detailed information for a completed service
    userId = session.get('userId')
    if not userId:
        return jsonify({"error": "User not logged in"}), 401

    try:
        # Use the same controller as for service history
        controller = SearchPastServiceController()
        # You might need to implement a method in your controller to get a single past service
        service = controller.getPastServiceById(service_id, userId)
        
        if not service:
            return jsonify({"error": "Service not found or not authorized"}), 404
        
        # Convert to dict if it's an object
        if hasattr(service, 'to_dict'):
            service_data = service.to_dict()
        else:
            service_data = service
            
        return jsonify(service_data)
    except Exception as e:
        # Log the detailed error for debugging
        import traceback
        print(f"Error getting service history detail: {str(e)}\n{traceback.format_exc()}")
        return jsonify({"error": "Server error processing service details"}), 500 