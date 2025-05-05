from app.Entities.service import Service

class ViewCategoryController:
    """
    Controller for viewing service categories
    """
    def __init__(self, db=None):
        """
        Initialize the controller with a database connection
        
        Args:
            db (ServiceCategoryDB, optional): Database connection. If None, creates a new one.
        """
        self.db = db if db is not None else Service()
    
    def get_all_categories(self):
        """
        Get all service categories
        
        Returns:
            list: All service categories
        """
        return self.db.get_all_categories()
        
        
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