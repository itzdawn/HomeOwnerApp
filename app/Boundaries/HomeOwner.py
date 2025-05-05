from flask import Blueprint, render_template
from app.Controllers.HomeOwner_related.ServiceDetails import ServiceDetailsController
from app.Controllers.HomeOwner_related.ServiceHistory import ServiceHistoryController
from app.Controllers.HomeOwner_related.ServiceHistorySearch import ServiceHistorySearchController
from app.Controllers.HomeOwner_related.ServiceSearch import ServiceSearchController
from app.Controllers.HomeOwner_related.ShortlistServices import ShortlistServicesController
from app.Controllers.HomeOwner_related.ShortlistViewer import ShortlistViewerController
from app.Controllers.HomeOwner_related.ShortlistSearch import ShortlistSearchController
from app.Boundaries.Login import login_required

homeowner_bp = Blueprint('homeowner', __name__)

@homeowner_bp.route('/dashboard', methods=['GET'])
@login_required
def dashboard():
    """Renders the homeowner dashboard/index page."""
    return render_template('LayoutIndex/HomeOwnerIndex.html')

@homeowner_bp.route('/service-search', methods=['GET'])
@login_required
def service_search():
    """Renders the service search page for homeowners."""
    return render_template('HomeOwnerMgntPage/ServiceSearch.html')

@homeowner_bp.route('/shortlisted-services', methods=['GET'])
@login_required
def shortlisted_services():
    """Renders the shortlisted services page for homeowners."""
    return render_template('HomeOwnerMgntPage/ShortlistedService.html')

@homeowner_bp.route('/service-history', endpoint='view_service_history')
@login_required
def service_history():
    """Renders the service history page for homeowners."""
    return render_template('HomeOwnerMgntPage/ServiceHistory.html')

@homeowner_bp.route('/available-services', methods=['GET'])
@login_required
def available_services():
    return ServiceDetailsController.get_available_services()

@homeowner_bp.route('/service-history/export', endpoint='export_service_history')
@login_required
def service_history():
    return ServiceHistoryController.get_service_history()


@homeowner_bp.route('/service-history/search', methods=['GET'])
@login_required
def search_service_history():
    return ServiceHistorySearchController.search_service_history()

@homeowner_bp.route('/service-search-by-id', methods=['GET'])
@login_required
def search_service_by_id():
    return ServiceSearchController.search_service_by_id()

@homeowner_bp.route('/shortlist/add', methods=['POST'])
@login_required
def add_to_shortlist():
    return ShortlistServicesController.add_to_shortlist()

@homeowner_bp.route('/shortlist/remove', methods=['POST'])
@login_required
def remove_from_shortlist():
    return ShortlistServicesController.remove_from_shortlist()

@homeowner_bp.route('/shortlisted-services', methods=['GET'])
@login_required
def view_shortlisted_services():
    return ShortlistViewerController.view_shortlisted_services()

@homeowner_bp.route('/shortlisted-services/search', methods=['GET'])
@login_required
def search_shortlisted_services():
    return ShortlistSearchController.search_shortlisted_services()