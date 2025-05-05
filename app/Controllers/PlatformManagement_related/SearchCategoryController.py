from app.Entities.service import Service

class SearchCategoryController:
    """
    Controller for searching service categories
    """
    def __init__(self, db=None):
        """
        Initialize the controller with a database connection
        
        Args:
            db (ServiceCategoryDB, optional): Database connection. If None, creates a new one.
        """
        self.db = db if db is not None else Service()
    
    def search_categories(self, search_term):
        """
        Search for categories by name or description
        
        Args:
            search_term (str): Term to search for in name or description
            
        Returns:
            list: Matched categories
        """
        if not search_term or len(search_term.strip()) == 0:
            return []
            
        return self.db.search_categories(search_term.strip())