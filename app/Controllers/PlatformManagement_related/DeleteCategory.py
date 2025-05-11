from app.Entities.serviceCategories import ServiceCategory

class DeleteCategoryController:
    
    def deleteCategory(self, id):
        try:
            response = ServiceCategory.deleteCategory(id)
            if response:
                return {"success": True, "message": "Service Category deleted successfully"}
            else:
                return {"success": False, "message": "Failed to delete service category"}
        except Exception as e:
            print(f"Error deleting service category: {str(e)}")
            return {"success": False, "message": f"Error: {str(e)}"}