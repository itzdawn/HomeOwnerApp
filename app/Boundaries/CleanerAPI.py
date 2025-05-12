from flask import Blueprint, jsonify, request, session
import traceback
from app.Controllers.PlatformManagement_related.ViewCategory import ViewCategoryController
from app.Controllers.Cleaner_related.CreateService import CreateServiceController
from app.Controllers.Cleaner_related.ViewService import ViewServiceController
from app.Controllers.Cleaner_related.DeleteService import DeleteServiceController
from app.Controllers.Cleaner_related.UpdateService import UpdateServiceController
from app.Controllers.Cleaner_related.SearchService import SearchServiceController
from app.Controllers.Cleaner_related.SearchPastService import SearchPastServiceController
from app.Controllers.Cleaner_related.ViewPastService import ViewPastServiceController
from app.Boundaries.Auth import login_required

cleaner_api_bp = Blueprint('cleaner_api', __name__)

#to dynamically load categories to select from when creating service.
@cleaner_api_bp.route('/service-categories', methods=['GET'])
def getServiceCategories():
    try:
        controller = ViewCategoryController()
        categories = controller.getAllCategories()
        return jsonify(categories), 200
    except Exception as e:
        print(f"[ERROR] Failed to get categories: {e}")
        return jsonify({'error': 'Server error'}), 500
    
#11 create service    
@cleaner_api_bp.route('/services', methods=['POST'])
@login_required
def createServiceApi():
    try:
        userId = session.get('userId')
        if not userId:
            return jsonify({"error": "User not logged in"}), 401

        data = request.get_json()
        if not data:
            return jsonify({"error": "Invalid input"}), 400

        controller = CreateServiceController()
        success = controller.createService(
            userId=userId,
            name=data.get('name'),
            description=data.get('description'),
            categoryId=data.get('categoryId'),
            price=float(data.get('price', 0))
        )

        if success:
            return jsonify({"success": True, "message": "Service created successfully"})
        else:
            return jsonify({"error": "Creation failed"}), 500
    except Exception as e:
        print(f"Error creating service: {str(e)}")
        return jsonify({"error": f"Server error: {str(e)}"}), 500

#15 search and display.
@cleaner_api_bp.route('/services', methods=['GET'])
@login_required
def searchServicesApi():
    try:
        userId = session.get('userId')
        if not userId:
            return jsonify({"error": "User not logged in"}), 401

        serviceId = request.args.get('service_id', type=int)
        serviceName = request.args.get('service_name')
        categoryId = request.args.get('categoryId')
        page = int(request.args.get('page', 1))
        items_per_page = int(request.args.get('items_per_page', 10))

        controller = SearchServiceController()

        if serviceId or serviceName or categoryId:
            services = controller.searchServices(userId=userId, serviceId=serviceId, serviceName=serviceName, categoryId=categoryId)
        else:
            services = controller.getAllServiceByUserId(userId)

        total_count = len(services)
        start_idx = (page - 1) * items_per_page
        end_idx = start_idx + items_per_page
        services_data = services[start_idx:end_idx]

        if services_data:
            print(f"[DEBUG] First service dict: {services_data[0]}")
        return jsonify({"services": services_data, "total": total_count}), 200

    except Exception as e:
        print(f"[searchServicesApi] Error: {e}")
        return jsonify({"error": "Server error"}), 500

#12, for view user details.
@cleaner_api_bp.route('/services/<int:service_id>', methods=['GET'])
@login_required
def getServiceById(service_id):
    try:
        controller = ViewServiceController()
        service = controller.getServiceByServiceId(service_id)
        if service:
            return jsonify(service), 200
        else:
            return jsonify({"error": "Service not found"}), 404
    except Exception as e:
        print(f"Error getting service: {str(e)}")
        return jsonify({"error": "Server error"}), 500


#13 update service details
@cleaner_api_bp.route('/services/<int:service_id>', methods=['PUT'])
@login_required
def updateServiceApi(service_id):
    try:
        userId = session.get('userId')
        if not userId:
            return jsonify({"error": "User not logged in"}), 401

        data = request.get_json()
        if not data:
            return jsonify({"error": "Invalid input"}), 400

        controller = UpdateServiceController()
        response = controller.updateService(
            serviceId=service_id,
            userId=userId,
            name=data.get('name'),
            description=data.get('description'),
            categoryId=data.get('categoryId'),  # Updated to match frontend
            price=float(data.get('price', 0))
        )

        if response.get('success'):
            return jsonify(response), 200
        else:
            return jsonify(response), 400
    except Exception as e:
        print(f"Error updating user: {str(e)}")
        return jsonify({"error": "Server error"}), 500


#14 delete service.
@cleaner_api_bp.route('/services/<int:service_id>', methods=['DELETE'])
@login_required
def deleteServiceApi(service_id):
    try:
        userId = session.get('userId')
        if not userId:
            return jsonify({"error": "User not logged in"}), 401

        controller = DeleteServiceController()
        response = controller.deleteService(service_id, userId)
        if response.get('success'):
            return jsonify(response), 200  # Return the result as JSON, with success
        else:
            return jsonify(response), 403

    except Exception as e:
        print(f"Error deleting service: {str(e)}")
        return jsonify({"error": f"Server error: {str(e)}"}), 500



#Past Service History-----------------------------------------------------------------------------------------------
@cleaner_api_bp.route('/service-history', methods=['GET'])
@login_required
def searchServiceHistoryApi():
    userId = session.get("userId")
    if not userId:
        return jsonify({"error": "User not logged in"}), 401

    # Extract filters from query parameters
    start_date = request.args.get("start_date")
    end_date = request.args.get("end_date")
    categoryId = request.args.get("categoryId", type=int)
    completed_service_id = request.args.get("id", type=int)
    service_name = request.args.get("service_name")

    # Pagination
    page = int(request.args.get('page', 1))
    items_per_page = int(request.args.get('items_per_page', 10))

    controller = SearchPastServiceController()

    try:
        if not (start_date or end_date or categoryId or completed_service_id or service_name):
            results = controller.getAllPastServices(userId)
        else:
            results = controller.searchPastServices(
                cleanerId=userId,
                startDate=start_date,
                endDate=end_date,
                categoryId=categoryId,
                completedServiceId=completed_service_id,
                name=service_name
            )

        # Handle errors returned from controller
        if isinstance(results, dict) and results.get("success") is False:
            return jsonify({"error": results.get("message", "Unknown error")}), 500

        total_count = len(results)
        start_idx = (page - 1) * items_per_page
        end_idx = start_idx + items_per_page
        paginated_results = results[start_idx:end_idx]

        return jsonify({
            "services": paginated_results,
            "total": total_count
        }), 200

    except Exception as e:
        import traceback
        print(f"[ERROR] Exception occurred: {str(e)}\n{traceback.format_exc()}")
        return jsonify({"error": "Server error processing service history"}), 500




@cleaner_api_bp.route('/completed-service/<int:service_id>', methods=['GET'])
@login_required
def getCompletedServiceById(service_id):
    controller = ViewPastServiceController()
    try:
        result = controller.getPastServiceById(service_id)
        if result:
            return jsonify(result), 200
        return jsonify({"error": "Service not found"}), 404
    except Exception as e:
        print(f"[ERROR] {e}\n{traceback.format_exc()}")
        return jsonify({"error": "Server error"}), 500