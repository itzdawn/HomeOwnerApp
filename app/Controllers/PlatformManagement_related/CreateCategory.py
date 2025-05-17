from app.Entities.serviceCategories import ServiceCategory

class CreateCategoryController:
    def createCategory(self, name, description):
        if not name or len(name.strip()) == 0:
            return {"message": "Invalid category name", "status": "error"}
            
        name = name.strip()
        description = description.strip() if description else ""
            
        category = ServiceCategory(name=name, description=description)
        return category.createCategory()
