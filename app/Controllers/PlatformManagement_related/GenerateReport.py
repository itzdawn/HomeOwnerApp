from app.Entities.completedService import CompletedService

class GenerateReportController:
    def generateReport(self, reportType, dateValue, groupBy):
        reportData = CompletedService.generateReport(reportType, dateValue, groupBy)

        if reportData is None:
            return None

        displayNames = {
            'category': 'Category',
            'service': 'Service',
            'cleaner': 'Cleaner',
            'homeowner': 'Homeowner'
        }

        displayLabel = displayNames.get(groupBy, groupBy.capitalize())
        title = f"{reportType.capitalize()} Report by {displayLabel}"
        headers = [displayLabel, "Total Services Used"]
        rows = [[entry['groupKey'], entry['totalServicesUsed']] for entry in reportData]
        total = sum(entry['totalServicesUsed'] for entry in reportData)
        totals = ["Total", total]

        return {
            "title": title,
            "headers": headers,
            "rows": rows,
            "totals": totals
        }
