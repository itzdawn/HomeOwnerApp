from app.Entities.service import Service

class DeleteCategoryController:
    """
    Controller for deleting service categories
    """
    def __init__(self, db=None):
        """
        Initialize the controller with a database connection
        
        Args:
            db (ServiceCategoryDB, optional): Database connection. If None, creates a new one.
        """
        self.db = db if db is not None else Service()
    
    def delete_category(self, id):
        """
        Delete a category by ID
        
        Args:
            id (int): ID of the category to delete
            
        Returns:
            bool: True if deletion successful, False if category not found
        """
        try:
            id = int(id)
            return self.db.delete_category(id)
        except (ValueError, TypeError):
            return False