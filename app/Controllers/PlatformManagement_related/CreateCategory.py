from app.Entities.serviceCategories import ServiceCategory

class CreateCategoryController:
    def createCategory(self, name, description):
        try:
            if not name or len(name.strip()) == 0:
                return {"message": "Invalid category name", "status": "error"}
            
            name = name.strip()
            description = description.strip() if description else ""
            
            category = ServiceCategory(name=name, description=description)
            response = category.createCategory()
            if response:
                return {"message": f"Service Category: {name} created successfully", "success": True}
            else:
                return {"message": f"Unable to create service category: {name}", "success": False}
        except Exception as e:
            print(f"Error creating service category: {str(e)}")
            return {"success": False, "message": f"Error: {str(e)}"}