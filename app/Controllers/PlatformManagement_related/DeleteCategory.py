from app.Entities.serviceCategories import ServiceCategory

class DeleteCategoryController:
    
    def deleteCategory(self, id):
        return ServiceCategory.deleteCategory(id)
 