from flask import Blueprint, request, jsonify, render_template
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
