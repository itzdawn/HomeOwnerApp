from app.Entities.serviceCategories import ServiceCategory

class ViewCategoryController:
    #currently used by cleaner.
    def getAllCategories(self):
        try:
            return ServiceCategory.getCategoryNames()
        except Exception as e:
            print(f"[Error] Unable to retrieve category names: {str(e)}")
            return []

        
    def getCategoryById(self, categoryId):
        try:
            category = ServiceCategory.getCategoryById(categoryId)
            if category:
                return category.toDict()
            else:
                return None
        except Exception as e:
            print(f"[ViewCategoryController] Fetch Error: {e}")
            return None