from flask import Blueprint, render_template, session, redirect, url_for
from app.Boundaries.Login import login_required

layout_bp = Blueprint('layout', __name__)

@layout_bp.route('/navbar', methods=['GET'])
def navbar():
    # Return the navbar template
    return render_template('LayoutPartials/Navbar.html')

@layout_bp.route('/sidebar', methods=['GET'])
def sidebar():
    # Get user role from session and render appropriate sidebar
    role = session.get('userRole', '')
    if not role:
        # No role in session → redirect to login page
        return redirect(url_for('index'))
    
    # Convert role to lowercase for consistent comparison
    role = role.lower()
    
    if role == 'admin':
        return render_template('LayoutPartials/AdminSidebar.html')
    elif role == 'cleaner':
        return render_template('LayoutPartials/CleanerSidebar.html')
    elif role == 'homeowner':
        return render_template('LayoutPartials/HomeownerSidebar.html')
    elif role == 'platformmanagement':
        return render_template('LayoutPartials/PlatformManagementSidebar.html')
    else:
        return redirect(url_for('index'))
