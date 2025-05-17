from flask import Blueprint, render_template
from app.Boundaries.Auth import login_required

platform_bp = Blueprint('platform', __name__)

@platform_bp.route('/dashboard', methods=['GET'])
@login_required
def dashboard():
    """Renders the platform management dashboard/index page."""
    return render_template('LayoutIndex/PlatformMgntIndex.html')

@platform_bp.route('/service-categories', methods=['GET'])
@login_required
def service_categories():
    """Renders the service categories management page."""
    return render_template('PlatformMgntPage/ServiceCategories.html')

@platform_bp.route('/reports', methods=['GET'])
@login_required
def reports():
    """Renders the reports generation page."""
    return render_template('PlatformMgntPage/Reports.html')
