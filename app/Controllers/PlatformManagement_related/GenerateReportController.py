from app.Entities.completedService import CompletedService
from datetime import datetime, timedelta

class GenerateReportController:
    """
    Controller for generating service usage reports
    Handles daily, weekly, monthly and custom date range reports
    """
    
    def __init__(self, db=None):
        """
        Initialize the controller with a database connection
        
        Args:
            db (CompletedService, optional): Database connection. If None, creates a new one.
        """
        self.db = db if db is not None else CompletedService
    
    def generate_report(self, report_type, date_value=None, group_by="category"):
        """
        Generate a service usage report based on parameters
        
        Args:
            report_type (str): Type of report - 'daily', 'weekly', 'monthly', or 'custom'
            date_value (str): Date string for the report period - single date or range
            group_by (str): How to group the report data - 'category', 'service', 'cleaner', 'homeowner'
            
        Returns:
            dict: Report data including title, headers, rows and totals
        """
        try:
            # Calculate date range based on report type
            start_date, end_date = self._calculate_date_range(report_type, date_value)
            
            # Get report data from database
            report_data = self.db.get_service_report(start_date, end_date, group_by)
            
            # Format report data
            title = self._generate_report_title(report_type, start_date, end_date, group_by)
            headers = self._generate_report_headers(group_by)
            
            # Return formatted report
            return {
                "title": title,
                "headers": headers,
                "rows": report_data.get("rows", []),
                "totals": report_data.get("totals", [])
            }
            
        except Exception as e:
            print(f"[GenerateReportController] Error generating report: {e}")
            return None
    
    def _calculate_date_range(self, report_type, date_value):
        """
        Calculate start and end dates for the report
        
        Args:
            report_type (str): Type of report
            date_value (str): Date string provided by user
            
        Returns:
            tuple: (start_date, end_date) formatted as strings
        """
        today = datetime.now()
        date_format = "%Y-%m-%d"
        
        if report_type == "daily":
            # For daily report: use provided date or today
            report_date = today
            if date_value:
                try:
                    report_date = datetime.strptime(date_value, date_format)
                except ValueError:
                    pass
            
            return (
                report_date.strftime(date_format),
                report_date.strftime(date_format)
            )
            
        elif report_type == "weekly":
            # For weekly report: 7 days before the selected date
            end_date = today
            if date_value:
                try:
                    end_date = datetime.strptime(date_value, date_format)
                except ValueError:
                    pass
            
            start_date = end_date - timedelta(days=6)
            return (
                start_date.strftime(date_format),
                end_date.strftime(date_format)
            )
            
        elif report_type == "monthly":
            # For monthly report: 30 days before the selected date
            end_date = today
            if date_value:
                try:
                    end_date = datetime.strptime(date_value, date_format)
                except ValueError:
                    pass
            
            start_date = end_date - timedelta(days=29)
            return (
                start_date.strftime(date_format),
                end_date.strftime(date_format)
            )
            
        elif report_type == "custom" and date_value:
            # For custom range: parse the range
            try:
                date_parts = date_value.split(" to ")
                if len(date_parts) == 2:
                    start_date = datetime.strptime(date_parts[0], date_format)
                    end_date = datetime.strptime(date_parts[1], date_format)
                    return (
                        start_date.strftime(date_format),
                        end_date.strftime(date_format)
                    )
            except ValueError:
                pass
        
        # Default: return today as both start and end date
        return (
            today.strftime(date_format),
            today.strftime(date_format)
        )
    
    def _generate_report_title(self, report_type, start_date, end_date, group_by):
        """
        Generate report title based on parameters
        
        Returns:
            str: Formatted report title
        """
        report_type_name = {
            "daily": "Daily",
            "weekly": "Weekly",
            "monthly": "Monthly",
            "custom": "Custom"
        }.get(report_type, "Custom")
        
        group_by_name = {
            "category": "Service Category",
            "service": "Service",
            "cleaner": "Cleaner",
            "homeowner": "Home Owner"
        }.get(group_by, "Category")
        
        if start_date == end_date:
            date_part = f"for {start_date}"
        else:
            date_part = f"from {start_date} to {end_date}"
            
        return f"{report_type_name} Service Usage Report by {group_by_name} {date_part}"
    
    def _generate_report_headers(self, group_by):
        """
        Generate report headers based on grouping
        
        Returns:
            list: Column headers for the report
        """
        if group_by == "category":
            return ["Category", "Services Completed", "Total Revenue ($)"]
        elif group_by == "service":
            return ["Service Name", "Bookings", "Total Revenue ($)"]
        elif group_by == "cleaner":
            return ["Cleaner Name", "Services Completed", "Total Revenue ($)"]
        elif group_by == "homeowner":
            return ["Home Owner", "Services Booked", "Total Spent ($)"]
        else:
            return ["Group", "Count", "Revenue ($)"] 