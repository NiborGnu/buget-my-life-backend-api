from django.core.management.base import BaseCommand
from categories.models import Category

class Command(BaseCommand):
    help = 'Populate the database with default categories'

    def handle(self, *args, **kwargs):
        # Define categories and their subcategories
        categories = {
            "Housing": {
                "type": "expense",
                "subcategories": [
                    "Rent/Mortgage",
                    "Electricity",
                    "Water",
                    "Trash",
                    "Internet",
                    "Maintenance",
                    "Property Tax",
                    "Others"
                ]
            },
            "Transportation": {
                "type": "expense",
                "subcategories": [
                    "Fuel",
                    "Car Payment",
                    "Insurance",
                    "Public Transit",
                    "Parking",
                    "Others"
                ]
            },
            "Food": {
                "type": "expense",
                "subcategories": [
                    "Groceries",
                    "Dining Out",
                    "Snacks",
                    "Beverages",
                    "Others"
                ]
            },
            "Health": {
                "type": "expense",
                "subcategories": [
                    "Doctor Visits",
                    "Medication",
                    "Dental Care",
                    "Gym",
                    "Others"
                ]
            },
            "Personal": {
                "type": "expense",
                "subcategories": [
                    "Clothing",
                    "Haircuts",
                    "Skincare",
                    "Entertainment",
                    "Hobbies",
                    "Others"
                ]
            },
            "Education": {
                "type": "expense",
                "subcategories": [
                    "Tuition",
                    "Books",
                    "Supplies",
                    "Courses",
                    "Others"
                ]
            },
            "Savings": {
                "type": "expense",
                "subcategories": [
                    "Emergency Fund",
                    "Retirement",
                    "Investments",
                    "Others"
                ]
            },
            "Debt": {
                "type": "expense",
                "subcategories": [
                    "Credit Cards",
                    "Student Loans",
                    "Personal Loans",
                    "Others"
                ]
            },
            "Miscellaneous": {
                "type": "expense",
                "subcategories": [
                    "Subscriptions",
                    "Donations",
                    "Gifts",
                    "Others"
                ]
            },
            "Employment": {
                "type": "income",
                "subcategories": [
                    "Salary",
                    "Bonuses",
                    "Overtime",
                    "Others"
                ]
            },
            "Investments": {
                "type": "income",
                "subcategories": [
                    "Dividends",
                    "Interest",
                    "Capital Gains",
                    "Others"
                ]
            },
            "Business": {
                "type": "income",
                "subcategories": [
                    "Sales",
                    "Freelance",
                    "Royalties",
                    "Others"
                ]
            },
            "Government": {
                "type": "income",
                "subcategories": [
                    "Tax Refund",
                    "Unemployment",
                    "Social Security",
                    "Others"
                ]
            },
            "Miscellaneous Income": {
                "type": "income",
                "subcategories": [
                    "Gifts",
                    "Inheritance",
                    "Others"
                ]
            },
        }

        # Use a set to track already created categories and subcategories
        existing_categories = set(
            Category.objects.values_list('name', flat=True)
        )

        for category_name, category_info in categories.items():
            # Create the main category if it doesn't exist
            if category_name not in existing_categories:
                # Create the category and log the creation
                main_category = Category.objects.create(
                    name=category_name,
                    category_type=category_info["type"]
                )
                existing_categories.add(category_name)
                self.stdout.write(
                    self.style.SUCCESS(
                        f'Created category: {category_name}'
                    )
                )

                # Create subcategories
                for subcategory_name in category_info["subcategories"]:
                # Check if subcategory already exists under the parent category
                    if (subcategory_name not in existing_categories and 
                        not Category.objects.filter(
                            name=subcategory_name, 
                            parent_category=main_category).exists()):
                        # Create the subcategory and log the creation
                        Category.objects.create(
                            name=subcategory_name,
                            category_type=category_info["type"],
                            parent_category=main_category
                        )
                        existing_categories.add(subcategory_name)
                        self.stdout.write(
                            self.style.SUCCESS(
                                f'Created subcategory: {subcategory_name} '
                                f'under {category_name}'
                            )
                        )

        self.stdout.write(
            self.style.SUCCESS(
                'Default categories and subcategories populated '
                'successfully!'
            )
        )
