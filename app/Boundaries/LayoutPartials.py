from flask import Blueprint, render_template, session, redirect, url_for
from app.Boundaries.Login import login_required

layout_bp = Blueprint('layout', __name__)

@layout_bp.route('/navbar', methods=['GET'])
def navbar():
    # Return the navbar template
    return render_template('LayoutPartials/Navbar.html')

@layout_bp.route('/sidebar', methods=['GET'])
def sidebar():
    # Get user profile from session and render appropriate sidebar
    profile = session.get('userProfile', '')
    if not profile:
        # No profile in session → redirect to login page
        return redirect(url_for('index'))
    
    # Convert profile to lowercase for consistent comparison
    profile = profile.lower()
    
    if profile == 'admin':
        return render_template('LayoutPartials/AdminSidebar.html')
    elif profile == 'cleaner':
        return render_template('LayoutPartials/CleanerSidebar.html')
    elif profile == 'homeowner':
        return render_template('LayoutPartials/HomeownerSidebar.html')
    elif profile == 'platformmanagement':
        return render_template('LayoutPartials/PlatformManagementSidebar.html')
    else:
        return redirect(url_for('index'))
