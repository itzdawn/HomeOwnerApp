from flask import *
from app.Controllers.Cleaner_related.CreateService import CreateServiceController
from app.Controllers.Cleaner_related.DeleteService import DeleteServiceController
from app.Controllers.Cleaner_related.SearchService import SearchServiceController
from app.Controllers.Cleaner_related.UpdateService import UpdateServiceController
from app.Controllers.Cleaner_related.ViewService import ViewServiceController
from app.Controllers.Cleaner_related.SearchPastService import SearchPastServiceController
from app.Boundaries.Login import login_required

cleaner_bp = Blueprint('cleaner', __name__)

@cleaner_bp.route('/dashboard', methods=['GET'])
@login_required
def dashboard():
    return render_template('LayoutIndex/CleanerIndex.html')

@cleaner_bp.route('/service-management', methods=['GET'])
@login_required
def service_management():
    return render_template('CleanerMgntPage/ServiceMgnt.html')

@cleaner_bp.route('/service-history', methods=['GET'])
@login_required
def service_history():
    return render_template('CleanerMgntPage/ServiceHistory.html')


#REQUIRES INTEGRATION WITH WEBPAGE ---------------------------

@cleaner_bp.route('/service/create', methods=['POST'])
def createService():
    controller = CreateServiceController()
    response = controller.createService(
        userId=request.form['userId'],
        name=request.form['name'],
        description=request.form['description'],
        category=request.form['category'],
        price=float(request.form['price'])
    )
    if response:
        return redirect("CREATESERVICE.HTML")
    else:
        return "Service creation failed", 500

@cleaner_bp.route('/my-services', methods=['GET'])
def getServices():
    userId = session.get('userId')
    controller = ViewServiceController()
    services = controller.getServiceByUserId(userId)
    if services is None:
        return "Failed to load services", 500

    return render_template('MyServices.html', services=services)

@cleaner_bp.route('/service/edit/<int:service_id>', methods=['GET'])
def editService(serviceId):
    controller = UpdateServiceController()
    service = controller.getServiceByServiceId(serviceId)
    if not service:
        return "Service not found or not authorized", 500

    return render_template('EditService.html', service=service)

@cleaner_bp.route('/service/update', methods=['POST'])
def updateService():
    userId = session.get('userId')
    serviceId = request.form['id']
    name = request.form['name']
    description = request.form['description']
    category = request.form['category']
    price = request.form['price']

    controller = UpdateServiceController()
    success = controller.updateService(
        serviceId=serviceId,
        userId=userId,
        name=name,
        description=description,
        category=category,
        price=price
    )

    if success:
        return render_template('showServices.html')
    else:
        return "Update failed", 500

@cleaner_bp.route('/service/delete/<int:serviceId>', methods=['POST'])
def delete_service(serviceId):
    userId = session.get('userId')
    controller = DeleteServiceController()
    success = controller.delete(serviceId, userId)

    if success:
        return render_template('showServices.html')
    else:
        return "Delete failed or unauthorized", 500

@cleaner_bp.route('/services/search')
def searchServices():
    keyword = request.args.get('q', '')
    userId = session.get('userId')
    controller = SearchServiceController()
    results = controller.searchServices(keyword)

    return render_template('SearchResults.html', services=results, current_user_id=userId, keyword=keyword)

@cleaner_bp.route('/services/past', methods=["GET", "POST"])
def search_past_services():
    userId = session.get("userId")

    start_date = request.form.get("start_date") or None
    end_date = request.form.get("end_date") or None
    category = request.form.get("category") or None

    controller = SearchPastServiceController()
    results = controller.searchPastServices(userId, start_date, end_date, category)

    return render_template("PastServices.html", services=results, filters={
        "start_date": start_date,
        "end_date": end_date,
        "category": category
    })