from flask import Blueprint, jsonify, request, session
from app.Controllers.HomeOwner_related.SearchAvailServices import SearchAvailServiceController
from app.Controllers.HomeOwner_related.ViewAvailServices import ViewAvailServiceController
from app.Controllers.HomeOwner_related.ViewServiceHistory import ViewServiceHistoryController
from app.Controllers.HomeOwner_related.SearchServiceHistory import SearchServiceHistoryController
from app.Controllers.HomeOwner_related.SearchShortlist import SearchShortlisthController
from app.Controllers.HomeOwner_related.ShortlistServices import ShortlistController
from app.Controllers.HomeOwner_related.ViewShortlistedService import ShortlistViewerController
from app.Boundaries.Auth import login_required

homeowner_api_bp = Blueprint('homeowner_api', __name__)

#26 search and display all available services
@homeowner_api_bp.route('/available-services', methods=['GET'])
@login_required
def searchAvailServicesApi():
    try:
        serviceName = request.args.get('service_name')
        categoryId = request.args.get('categoryId', type=int)
        page = int(request.args.get('page', 1))
        items_per_page = int(request.args.get('items_per_page', 10))
        
        controller = SearchAvailServiceController()
        
        if serviceName or categoryId:
            services = controller.SearchAvailServices(serviceName, categoryId)
        else:
            services = controller.getAllAvailServices()
        
        total_count = len(services)
        start_idx = (page - 1) * items_per_page
        end_idx = start_idx + items_per_page
        service_data = services[start_idx:end_idx]

        return jsonify({"services": service_data, "total": total_count}), 200

    except Exception as e:
        print(f"[searchServicesApi] Error: {e}")
        return jsonify({"error": "Server error"}), 500

#27 view service details in the services available
@homeowner_api_bp.route('/services/<int:service_id>', methods=['GET'])
@login_required
def getServiceById(service_id):
    try:
        controller = ViewAvailServiceController()
        service = controller.getAvailServiceByServiceId(service_id)
        if service:
            return jsonify(service), 200
        else:
            return jsonify({"error": "Service not found"}), 404
    except Exception as e:
        print(f"Error getting service (homeowner): {str(e)}")
        return jsonify({"error": "Server error"}), 500

#50 search and display shortlisted services
@homeowner_api_bp.route('/shortlisted-services', methods=['GET'])
@login_required
def searchShortlistsApi():
    try:
        homeownerId = session.get('userId')
        serviceName = request.args.get('service_name')
        categoryId = request.args.get('categoryId', type=int)
        page = int(request.args.get('page', 1))
        items_per_page = int(request.args.get('items_per_page', 10))
        
        controller = SearchShortlisthController()
        
        if serviceName or categoryId:
            services = controller.searchShortlistedServices(homeownerId=homeownerId,serviceName=serviceName, categoryId=categoryId)
        else:
            services = controller.getShortlists(homeownerId=homeownerId)
        
        total_count = len(services)
        start_idx = (page - 1) * items_per_page
        end_idx = start_idx + items_per_page
        service_data = services[start_idx:end_idx]

        return jsonify({"services": service_data, "total": total_count}), 200

    except Exception as e:
        print(f"[searchServicesApi] Error: {e}")
        return jsonify({"error": "Server error"}), 500

#28 view shortlisted service details
@homeowner_api_bp.route('/shortlisted-services/<int:service_id>', methods=['GET'])
@login_required
def getShortlistedServiceById(service_id):
    try:
        homeownerId = session.get('userId')
        controller = ShortlistViewerController()
        service = controller.getShortlistedServiceDetail(service_id, homeownerId)
        
        if service:
            return jsonify(service), 200
        else:
            return jsonify({"error": "Service not found in shortlist"}), 404
    except Exception as e:
        print(f"[getShortlistedServiceById] Error: {e}")
        return jsonify({"error": "Server error"}), 500
    
#41 shortlist service
@homeowner_api_bp.route('/shortlist', methods=['POST'])
@login_required
def addShortlistApi():
    try:
        homeOwnerId = session.get('userId')
        serviceId = request.form.get('service_id', type=int)

        if not serviceId:
            return jsonify({"error": "Service ID is required"}), 400

        controller = ShortlistController()
        result = controller.addShortlist(homeOwnerId, serviceId)

        if result["success"]:
            return jsonify({"message": "Service shortlisted successfully!"}), 201
        else:
            return jsonify({"error": result["message"]}), 400
    except Exception as e:
        print(f"[addShortlist] Error: {e}")
        return jsonify({"error": "Server error"}), 500

@homeowner_api_bp.route('/shortlist/<int:serviceId>', methods=['DELETE'])
@login_required
def removeShortlistApi(serviceId):
    try:
        homeOwnerId = session.get('userId')

        controller = ShortlistController()
        result = controller.removeShortlist(homeOwnerId, serviceId)

        if result["success"]:
            return jsonify({"message": result["message"]}), 200
        else:
            return jsonify({"error": result["message"]}), 400
    except Exception as e:
        print(f"[removeShortlistApi] Error: {e}")
        return jsonify({"error": "Server error"}), 500

#29 search and display all completed services.
@homeowner_api_bp.route('/completed-services', methods=['GET'])
@login_required
def searchCompletedServicesApi():
    userId = session.get("userId")
    if not userId:
        return jsonify({"error": "User not logged in"}), 401

    # Filters
    serviceName = request.args.get("service_name")
    categoryId = request.args.get("categoryId", type=int)
    startDate = request.args.get("start_date")
    endDate = request.args.get("end_date")

    #Pagination
    page = int(request.args.get('page', 1))
    items_per_page = int(request.args.get('items_per_page', 10))

    controller = SearchServiceHistoryController()

    try:
        if serviceName or categoryId or startDate or endDate:
            results = controller.searchCompletedServices(
                homeownerId=userId,
                name=serviceName,
                categoryId=categoryId,
                startDate=startDate,
                endDate=endDate
            )
        else:
            results = controller.getAllCompletedServices(userId)

        #Pagination
        total_count = len(results)
        paginated = results[(page - 1) * items_per_page : page * items_per_page]

        return jsonify({"services": paginated, "total": total_count}), 200

    except Exception as e:
        print(f"[searchCompletedServicesApi] Error: {str(e)}")
        return jsonify({"error": "Server error"}), 500

#30 view service history
@homeowner_api_bp.route('/service-history/<int:service_id>', methods=['GET'])
@login_required
def getCompletedServiceByIdApi(service_id):
    controller = ViewServiceHistoryController()
    try:
        result = controller.getCompletedServiceById(service_id)
        if result:
            return jsonify(result), 200
        return jsonify({"error": "Service not found"}), 404
    except Exception as e:
        print(f"[ERROR] {e}")
        return jsonify({"error": "Server error"}), 500