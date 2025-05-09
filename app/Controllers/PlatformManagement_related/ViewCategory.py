from app.Entities.serviceCategories import ServiceCategory

class ViewCategoryController:
    
    def __init__(self):
        pass
    
    def getAllCategories(self):
        try:
            return ServiceCategory.getCategoryNames()
        except Exception as e:
            print(f"[Error] Unable to retrieve category names: {str(e)}")
            return []

        
    def get_category_by_id(self, id):
        """
        Find a category by its ID
        
        Args:
            id (int): The ID of the category to find
            
        Returns:
            ServiceCategory or None: The found category or None if not found
        """
        try:
            id = int(id)
            return self.db.get_category_by_id(id)
        except (ValueError, TypeError):
            return None