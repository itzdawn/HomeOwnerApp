from app.Entities.service import Service

class CreateCategoryController:
    """
    Controller for creating service categories
    """
    def __init__(self, db=None):
        """
        Initialize the controller with a database connection
        
        Args:
            db (ServiceCategoryDB, optional): Database connection. If None, creates a new one.
        """
        self.db = db if db is not None else Service()
    
    def create_category(self, name, description):
        """
        Create a new service category
        
        Args:
            name (str): Name of the service category
            description (str): Description of the service category
            
        Returns:
            dict: The newly created category, or a failure message
        """
        # Validate input
        if not name or len(name.strip()) == 0:
            raise ValueError("Category name cannot be empty")
        
        # Trim whitespace
        name = name.strip()
        description = description.strip() if description else ""
        
        # Create the category
        inserted_category = self.db.insert_category(name, description)
        
        if inserted_category:
            return {"message": "Category successfully created", "category": inserted_category}
        else:
            return {"message": "Category creation failed"}
