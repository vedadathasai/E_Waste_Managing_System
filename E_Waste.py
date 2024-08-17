from datetime import datetime, timedelta

class ElectronicItem:
    def __init__(self, name, purchase_date, lifespan_years, maintenance_cost, resale_value):
        self.name = name
        self.purchase_date = purchase_date
        self.lifespan_years = lifespan_years
        self.maintenance_cost = maintenance_cost
        self.resale_value = resale_value

    def remaining_life_years(self):
        expected_end_date = self.purchase_date + timedelta(days=self.lifespan_years * 365)
        remaining_time = expected_end_date - datetime.now()
        return max(remaining_time.days / 365.0, 0)

    def is_due_for_replacement(self):
        return self.remaining_life_years() == 0

    def is_profitable_to_maintain(self):
        return self.resale_value > self.maintenance_cost

    def profit_from_replacement(self):
        return self.resale_value - self.maintenance_cost

    def __str__(self):
        return (f"{self.name} (Purchased: {self.purchase_date.date()}, Lifespan: {self.lifespan_years} years, "
                f"Maintenance Cost: ${self.maintenance_cost}, Resale Value: ${self.resale_value}, "
                f"Remaining Life: {self.remaining_life_years():.2f} years)")

class EwasteMonitor:
    def __init__(self):
        self.items = []

    def add_item(self, item):
        self.items.append(item)

    def check_items(self):
        due_for_replacement = []
        profitable_to_keep = []
        for item in self.items:
            # Only suggest replacement if the remaining life is low or maintaining is not profitable
            if item.remaining_life_years() < 1 or not item.is_profitable_to_maintain():
                if item.profit_from_replacement() > 0 or item.is_due_for_replacement():
                    due_for_replacement.append(item)
            else:
                profitable_to_keep.append(item)
        return due_for_replacement, profitable_to_keep

    def generate_report(self):
        report = "E-waste Monitoring Report:\n"
        due_for_replacement, profitable_to_keep = self.check_items()

        if due_for_replacement:
            report += "\nItems suggested for replacement (based on profit or end of life):\n"
            for item in due_for_replacement:
                report += f" - {item}\n"
        else:
            report += "\nNo items suggested for replacement.\n"

        if profitable_to_keep:
            report += "\nItems profitable to maintain:\n"
            for item in profitable_to_keep:
                report += f" - {item}\n"
        else:
            report += "\nNo items profitable to maintain.\n"

        return report

# Example usage
monitor = EwasteMonitor()

# Add electronic items
monitor.add_item(ElectronicItem("Laptop (New Model)", datetime(2023, 1, 1), 5, maintenance_cost=150, resale_value=1000))
monitor.add_item(ElectronicItem("Smartphone (New Model)", datetime(2024, 3, 1), 3, maintenance_cost=50, resale_value=600))
monitor.add_item(ElectronicItem("Old Desktop Computer", datetime(2015, 1, 1), 8, maintenance_cost=300, resale_value=50))
monitor.add_item(ElectronicItem("Printer (Old Model)", datetime(2017, 12, 1), 5, maintenance_cost=100, resale_value=20))

# Generate a report
print(monitor.generate_report())
