from flask import Blueprint, request, jsonify, render_template
from app.Boundaries.Auth import login_required

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/dashboard', methods=['GET'])
@login_required
def dashboard():
    return render_template('LayoutIndex/AdminIndex.html')

@admin_bp.route('/user-accounts', methods=['GET'])
@login_required
def user_accounts():
    return render_template('UserAdminPage/user-account.html')

@admin_bp.route('/user-profiles', methods=['GET'])
@login_required
def user_profiles():
    return render_template('UserAdminPage/user-profile.html')