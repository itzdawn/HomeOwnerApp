from app.Entities.serviceCategories import ServiceCategory

class UpdateCategoryController:

    def updateCategory(self, id, name=None, description=None):
        category = ServiceCategory.getCategoryById(id)
        if not category:
            return {"success": False, "message": "Category not found"}

        return category.updateCategory(name=name, description=description)
