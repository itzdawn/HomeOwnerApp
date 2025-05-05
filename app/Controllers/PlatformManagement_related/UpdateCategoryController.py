from app.Entities.service import Service

class UpdateCategoryController:
    """
    Controller for updating service categories
    """
    def __init__(self, db=None):
        """
        Initialize the controller with a database connection
        
        Args:
            db (ServiceCategoryDB, optional): Database connection. If None, creates a new one.
        """
        self.db = db if db is not None else Service()
    
    def update_category(self, id, name=None, description=None):
        """
        Update an existing category
        
        Args:
            id (int): ID of the category to update
            name (str, optional): New name for the category
            description (str, optional): New description for the category
            
        Returns:
            bool: True if update successful, False if category not found
        """
        try:
            id = int(id)
            
            # Validate input if provided
            if name is not None:
                if len(name.strip()) == 0:
                    raise ValueError("Category name cannot be empty")
                name = name.strip()
                
            if description is not None:
                description = description.strip()
            
            return self.db.update_category(id, name, description)
        except (ValueError, TypeError):
            return False