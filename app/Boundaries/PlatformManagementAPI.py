from flask import Blueprint, jsonify, request, session
from app.Controllers.PlatformManagement_related.CreateCategory import CreateCategoryController
from app.Controllers.PlatformManagement_related.DeleteCategory import DeleteCategoryController
from app.Controllers.PlatformManagement_related.UpdateCategory import UpdateCategoryController
from app.Controllers.PlatformManagement_related.SearchCategory import SearchCategoryController
from app.Controllers.PlatformManagement_related.ViewCategory import ViewCategoryController
from app.Controllers.PlatformManagement_related.GenerateReport import GenerateReportController
from app.Boundaries.Auth import login_required

platform_api_bp = Blueprint('platform_api', __name__)

#37 Service Categories API, Verified.
@platform_api_bp.route('/service-categories', methods=['GET'])
@login_required
def searchCategoriesApi():
    """Get all service categories or search by keyword"""
    try:
        # Get search parameters
        name = request.args.get('name')
        categoryId = request.args.get('categoryId', type=int)
        page = int(request.args.get('page', 1))
        items_per_page = int(request.args.get('items_per_page', 10))
        
        controller = SearchCategoryController()
        
        if name or categoryId:
            categories = controller.searchCategories(categoryId=categoryId, name=name)
        else:
            categories = controller.getAllCategories()
        
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
        }), 200
    except Exception as e:
        print(f"Error getting categories: {e}")
        return jsonify({"error": "Failed to get categories"}), 500

#34 viewing category details.
@platform_api_bp.route('/service-categories/<int:categoryId>', methods=['GET'])
@login_required
def getCategoryById(categoryId):
    """Get a single service category by ID"""
    try:
        controller = ViewCategoryController()
        category = controller.getCategoryById(categoryId)
        if category:
            return jsonify(category), 200
        else:
            return jsonify({"error": "Service not found"}), 404
    except Exception as e:
        print(f"Error getting category: {e}")
        return jsonify({"error": "Failed to get category"}), 500

#33 create service category
@platform_api_bp.route('/service-categories', methods=['POST'])
@login_required
def createCategoryApi():
    try:
        data = request.form
        name = data.get('name')
        description = data.get('description', '')
        
        if not name:
            return jsonify({"error": "Category name is required"}), 400
            
        controller = CreateCategoryController()
        response = controller.createCategory(name=name, description=description)
        
        if response.get('success'):
            return jsonify(response), 201
        else:
            return jsonify(response), 400
    except Exception as e:
        print(f"Error creating category: {e}")
        return jsonify({"error": "Server error"}), 500



@platform_api_bp.route('/service-categories/<int:categoryId>', methods=['PUT'])
@login_required
def updateCategoryApi(categoryId):
    try:
        data = request.form
        name = data.get('name')
        description = data.get('description', '')
        
        if not name:
            return jsonify({"error": "Category name is required"}), 400
            
        controller = UpdateCategoryController()
        response = controller.updateCategory(categoryId, name, description)
        
        if response.get('success'):
            return jsonify(response), 200
        else:
            return jsonify(response), 400
    except Exception as e:
        print(f"Error updating user: {str(e)}")
        return jsonify({"error": "Server error"}), 500

#36 delete service category
@platform_api_bp.route('/service-categories/<int:categoryId>', methods=['DELETE'])
@login_required
def deleteCategoryApi(categoryId):
    try:
        controller = DeleteCategoryController()
        response= controller.deleteCategory(categoryId)
        
        if response.get('success'):
            return jsonify(response), 200
        else:
            return jsonify(response), 403

    except Exception as e:
        print(f"Error deleting category: {e}")
        return jsonify({"error": "Server error"}), 500

# Reports API
@platform_api_bp.route('/reports', methods=['GET'])
@login_required
def generateReportApi():
    try:
        reportType = request.args.get('reportType', 'daily').lower()
        dateValue = request.args.get('dateValue')
        groupBy = request.args.get('groupBy', 'category').lower()

        if not dateValue:
            return jsonify({"error": "Missing required parameter: dateValue"}), 400

        validReportTypes = ['daily', 'weekly', 'monthly']
        validGroupBys = ['category', 'service', 'cleaner', 'homeowner']

        if reportType not in validReportTypes:
            return jsonify({"error": f"Invalid reportType. Choose from {validReportTypes}"}), 400

        if groupBy not in validGroupBys:
            return jsonify({"error": f"Invalid groupBy. Choose from {validGroupBys}"}), 400

        controller = GenerateReportController()
        result = controller.generateReport(reportType, dateValue, groupBy)

        if result:
            return jsonify(result), 200
        else:
            return jsonify({"error": "Failed to generate report"}), 500
        
    except Exception as e:
        print("Error generating report:", e)
        return jsonify({"error": "Server error"}), 500
