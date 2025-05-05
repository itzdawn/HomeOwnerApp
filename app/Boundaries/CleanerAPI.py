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
    category_id = request.args.get('category_id')
    
    # Get pagination parameters
    page = int(request.args.get('page', 1))
    items_per_page = int(request.args.get('items_per_page', 10))

    # Debug log the request parameters
    print(f"DEBUG - API request params: service_id={service_id}, service_name={service_name}, category_id={category_id}, page={page}")

    # Use enhanced filterServices method for efficient database filtering
    from app.Entities.service import Service
    services = Service.filterServices(
        userId=userId,
        serviceId=service_id,
        serviceName=service_name,
        category=category_id 
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
    
    # Debug log for first service to check data structure
    if services_data:
        print(f"DEBUG - First service data sample: {services_data[0]}")
        
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

@cleaner_api_bp.route('/services', methods=['POST'])
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

        # Log the incoming data for debugging
        print(f"DEBUG - Create service data: {data}")

        controller = CreateServiceController()
        success = controller.createService(
            userId=userId,
            name=data.get('name'),
            description=data.get('description'),
            category=data.get('category_id'),  # Use category_id from frontend
            price=float(data.get('price', 0))
        )

        if success:
            return jsonify({"success": True, "message": "Service created successfully"})
        else:
            return jsonify({"error": "Creation failed"}), 500
    except Exception as e:
        print(f"Error creating service: {str(e)}")
        return jsonify({"error": f"Server error: {str(e)}"}), 500

@cleaner_api_bp.route('/services/<int:service_id>', methods=['PUT'])
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

        # Log the incoming data for debugging
        print(f"DEBUG - Update service data: {data}")

        controller = UpdateServiceController()
        success = controller.updateService(
            serviceId=service_id,
            userId=userId,
            name=data.get('name'),
            description=data.get('description'),
            category=data.get('category_id'),  # Updated to match frontend
            price=float(data.get('price', 0))
        )

        if success:
            return jsonify({"success": True, "message": "Service updated successfully"})
        else:
            return jsonify({"error": "Update failed or unauthorized"}), 403
    except Exception as e:
        print(f"Error updating service: {str(e)}")
        return jsonify({"error": f"Server error: {str(e)}"}), 500

@cleaner_api_bp.route('/services/<int:service_id>', methods=['DELETE'])
@login_required
def delete_service_api(service_id):
    # Delete a service
    try:
        userId = session.get('userId')
        if not userId:
            return jsonify({"error": "User not logged in"}), 401

        controller = DeleteServiceController()
        result = controller.delete(service_id, userId)
        
        # Handle the new response format
        if isinstance(result, dict):
            # New format returns a dictionary with success and message
            if result.get('success'):
                return jsonify({"success": True, "message": result.get('message', 'Service deleted successfully')})
            else:
                return jsonify({"error": result.get('message', 'Delete failed or unauthorized')}), 403
        else:
            # Old format returns a boolean
            if result:
                return jsonify({"success": True, "message": "Service deleted successfully"})
            else:
                return jsonify({"error": "Delete failed or unauthorized"}), 403
    except Exception as e:
        print(f"Error deleting service: {str(e)}")
        return jsonify({"error": f"Server error: {str(e)}"}), 500

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
    service_date = request.args.get("service_date")
    category_id = request.args.get("category_id")
    service_id = request.args.get("service_id")  # Filter by SERVICE table ID
    completed_service_id = request.args.get("id")  # Filter by COMPLETED_SERVICE table ID
    service_name = request.args.get("service_name")
    
    # Get pagination parameters
    page = int(request.args.get('page', 1))
    items_per_page = int(request.args.get('items_per_page', 10))
    
    # Let the controller handle fetching and potentially filtering
    controller = SearchPastServiceController()
    try:
        # Log request parameters for debugging
        print(f"DEBUG - Search parameters: date={service_date}, category={category_id}, service_id={service_id}, completed_id={completed_service_id}, name={service_name}")
        
        # Pass the completed_service_id parameter to the controller
        results = controller.searchPastServices(userId, service_date, None, category_id, completed_service_id)
        
        if not results:
            return jsonify({"services": [], "total": 0})

        # Ensure each result has category name and homeowner name
        for item in results:
            # Make sure category_id is an integer
            if 'category_id' in item and item['category_id'] and not isinstance(item['category_id'], int):
                try:
                    item['category_id'] = int(item['category_id'])
                except (ValueError, TypeError):
                    pass
                    
            # If homeowner_name is not already included, try to get it
            if 'homeowner_name' not in item or not item['homeowner_name']:
                if 'homeowner_id' in item:
                    # This would require a separate function to get user details
                    # For now, we'll rely on the controller providing this info
                    pass
        
        # Convert results to dictionaries if they are objects
        if results and hasattr(results[0], 'to_dict'):
            processed_results = [item.to_dict() for item in results]
        else: # Assuming it might already be list of dicts
            processed_results = results

        # Optional: Apply secondary filters if controller didn't handle them
        filtered_results = []
        if service_id or service_name:
            for item in processed_results:
                # Check service_id filter
                if service_id and str(item.get('service_id', '')) != service_id:
                    continue
                # Check service_name filter (case-insensitive)
                # Ensure the key matches what the controller/to_dict returns
                service_name_in_item = item.get('service_name') or item.get('name')
                if service_name and (not service_name_in_item or service_name.lower() not in service_name_in_item.lower()):
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
        
        # Debug first result
        if paginated_results:
            print(f"DEBUG - First result in paginated data: {paginated_results[0]}")
        
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