from flask import Blueprint, render_template
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

@homeowner_bp.route('/service-history', methods=['GET'])
@login_required
def service_history():
    """Renders the service history page for homeowners."""
    return render_template('HomeOwnerMgntPage/ServiceHistory.html')
