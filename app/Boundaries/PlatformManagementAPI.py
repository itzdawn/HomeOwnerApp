from flask import Blueprint, jsonify, request, session
from app.Controllers.PlatformManagement_related.CreateCategoryController import CreateCategoryController
from app.Controllers.PlatformManagement_related.DeleteCategoryController import DeleteCategoryController
from app.Controllers.PlatformManagement_related.UpdateCategoryController import UpdateCategoryController
from app.Controllers.PlatformManagement_related.SearchCategoryController import SearchCategoryController
from app.Controllers.PlatformManagement_related.ViewCategory import ViewCategoryController
from app.Controllers.PlatformManagement_related.GenerateReportController import GenerateReportController
from app.Boundaries.Login import login_required

# Blueprint for all platform management API endpoints
platform_api_bp = Blueprint('platform_api', __name__)

# Service Categories API
@platform_api_bp.route('/service-categories', methods=['GET'])
@login_required
def get_categories_api():
    """Get all service categories or search by keyword"""
    try:
        # Get search parameter
        keyword = request.args.get('keyword', '')
        page = int(request.args.get('page', 1))
        items_per_page = int(request.args.get('items_per_page', 10))
        
        controller = SearchCategoryController() if keyword else ViewCategoryController()
        
        if keyword:
            categories = controller.search_categories(keyword)
        else:
            categories = controller.get_all_categories()
        
        # Implement pagination
        total = len(categories)
        start_idx = (page - 1) * items_per_page
        end_idx = start_idx + items_per_page
        paginated_categories = categories[start_idx:end_idx]
        
        return jsonify({
            'categories': paginated_categories,
            'total': total,
            'page': page,
            'items_per_page': items_per_page
        })
    except Exception as e:
        print(f"Error getting categories: {e}")
        return jsonify({"error": "Failed to get categories"}), 500

@platform_api_bp.route('/service-categories/<int:category_id>', methods=['GET'])
@login_required
def get_category_by_id(category_id):
    """Get a single service category by ID"""
    try:
        controller = ViewCategoryController()
        category = controller.get_category_by_id(category_id)
        
        if not category:
            return jsonify({"error": "Category not found"}), 404
            
        return jsonify(category)
    except Exception as e:
        print(f"Error getting category: {e}")
        return jsonify({"error": "Failed to get category"}), 500

@platform_api_bp.route('/service-categories', methods=['POST'])
@login_required
def create_category_api():
    """Create a new service category"""
    try:
        data = request.form
        name = data.get('name')
        description = data.get('description', '')
        
        if not name:
            return jsonify({"error": "Category name is required"}), 400
            
        controller = CreateCategoryController()
        category_id = controller.create_category(name, description)
        
        if not category_id:
            return jsonify({"error": "Failed to create category"}), 500
            
        return jsonify({
            "success": True,
            "message": "Category created successfully",
            "id": category_id
        }), 201
    except Exception as e:
        print(f"Error creating category: {e}")
        return jsonify({"error": "Server error"}), 500

@platform_api_bp.route('/service-categories/<int:category_id>', methods=['PUT'])
@login_required
def update_category_api(category_id):
    """Update an existing service category"""
    try:
        data = request.form
        name = data.get('name')
        description = data.get('description', '')
        
        if not name:
            return jsonify({"error": "Category name is required"}), 400
            
        controller = UpdateCategoryController()
        success = controller.update_category(category_id, name, description)
        
        if not success:
            return jsonify({"error": "Failed to update category"}), 500
            
        return jsonify({
            "success": True,
            "message": "Category updated successfully"
        })
    except Exception as e:
        print(f"Error updating category: {e}")
        return jsonify({"error": "Server error"}), 500

@platform_api_bp.route('/service-categories/<int:category_id>', methods=['DELETE'])
@login_required
def delete_category_api(category_id):
    """Delete a service category"""
    try:
        controller = DeleteCategoryController()
        success = controller.delete_category(category_id)
        
        if not success:
            return jsonify({
                "error": "Failed to delete category. It may be in use by existing services."
            }), 400
            
        return jsonify({
            "success": True,
            "message": "Category deleted successfully"
        })
    except Exception as e:
        print(f"Error deleting category: {e}")
        return jsonify({"error": "Server error"}), 500

# Reports API
@platform_api_bp.route('/reports', methods=['GET'])
@login_required
def generate_report_api():
    """Generate a service usage report"""
    try:
        # Get report parameters
        report_type = request.args.get('report_type', 'daily')
        date_value = request.args.get('date_value', None)
        group_by = request.args.get('group_by', 'category')
        
        # Validate parameters
        valid_report_types = ['daily', 'weekly', 'monthly', 'custom']
        valid_group_bys = ['category', 'service', 'cleaner', 'homeowner']
        
        if report_type not in valid_report_types:
            return jsonify({"error": "Invalid report type"}), 400
        
        if group_by not in valid_group_bys:
            return jsonify({"error": "Invalid grouping parameter"}), 400
            
        # Generate report
        controller = GenerateReportController()
        report_data = controller.generate_report(report_type, date_value, group_by)
        
        if not report_data:
            return jsonify({"error": "Failed to generate report"}), 500
            
        return jsonify(report_data)
    except Exception as e:
        print(f"Error generating report: {e}")
        return jsonify({"error": "Server error"}), 500 