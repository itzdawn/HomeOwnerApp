from app.Entities.serviceCategories import ServiceCategory

class UpdateCategoryController:

    def updateCategory(self, id, name=None, description=None):
        try:
            category = ServiceCategory.getCategoryById(id)
            if not category:
                return {"success": False, "message": "Category not found"}
            if name:
                category.name= name
            if description:
                category.description = description
            result = category.updateCategory()
            if result:
                return {"success": True, "message": "Category updated successfully"}
            else:
                return {"success": False, "message": "Failed to update category"}
                
        except Exception as e:
            print(f"Error updating category: {str(e)}")
            return {"success": False, "message": f"Error: {str(e)}"}
