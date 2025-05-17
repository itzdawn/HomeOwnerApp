from app.Entities.serviceCategories import ServiceCategory

class SearchCategoryController:
    
    def searchCategories(self, name=None, categoryId=None):
        try:
            Categories = ServiceCategory.searchServiceCategories(name, categoryId)
            return [c.toDict() for c in Categories]
        except Exception as e:
            print(f"[Error] Unable to retrieve categories: {str(e)}")
            return {"success": False, "message": f"Error: {str(e)}"}
    
    def getAllCategories(self):
        try:
            Categories = ServiceCategory.getAllCategories()
            return [c.toDict() for c in Categories]
        except Exception as e:
            print(f"[Error] Unable to retrieve user: {str(e)}")
            return []
        