import random
from datetime import datetime, timedelta
from django.core.management.base import BaseCommand
from api.models import Expense, Income, SavingGoal, ExpenseType, IncomeType, SavingGoalType
from django.contrib.auth.models import User

# Helper functions


def random_date(start, end):
    """Generate a random datetime between `start` and `end`"""
    return start + timedelta(
        seconds=random.randint(0, int((end - start).total_seconds())),
    )


class Command(BaseCommand):
    help = 'Populates the database with test data for expenses, income, and saving goals.'

    def handle(self, *args, **kwargs):
        # Create or get the test user
        user, created = User.objects.get_or_create(
            username='testuser1', email='test@example.com')
        if created:
            user.set_password('password1234')
            user.save()
        if created:
            self.stdout.write(self.style.SUCCESS('Created user "testuser1".'))
        else:
            self.stdout.write(self.style.SUCCESS(
                'User "testuser1" already exists.'))

        # Generating random test data for expenses
        for _ in range(50):
            Expense.objects.create(
                user=user,
                expense_type=random.choice([ExpenseType.FOOD, ExpenseType.TRANSPORT,
                                           ExpenseType.ENTERTAINMENT, ExpenseType.BILLS, ExpenseType.OTHER]),
                amount=round(random.uniform(10.0, 500.0), 2),
                date=random_date(datetime(2024, 1, 1), datetime(2024, 9, 18)),
                description=random.choice(
                    ["Lunch", "Bus fare", "Movie night", "Electricity bill", "Groceries"])
            )

        # Generating random test data for income
        for _ in range(10):
            Income.objects.create(
                user=user,
                income_type=random.choice(
                    [IncomeType.SALARY, IncomeType.FREELANCE, IncomeType.INVESTMENT, IncomeType.GIFT, IncomeType.OTHER]),
                amount=round(random.uniform(500.0, 3000.0), 2),
                date=random_date(datetime(2024, 1, 1), datetime(2024, 9, 15)),
                description=random.choice(
                    ["Monthly salary", "Freelance project", "Investment return", "Birthday gift"])
            )

        # Generating random test data for saving goals
        SavingGoal.objects.create(
            user=user,
            goal_type=SavingGoalType.VACATION,
            target_amount=2000.00,
            accumulated_amount=500.00,
            start_date=datetime(2024, 1, 1),
            end_date=datetime(2024, 12, 31)
        )

        SavingGoal.objects.create(
            user=user,
            goal_type=SavingGoalType.EMERGENCY,
            target_amount=5000.00,
            accumulated_amount=1500.00,
            start_date=datetime(2024, 2, 1),
            end_date=None  # No end date
        )

        SavingGoal.objects.create(
            user=user,
            goal_type=SavingGoalType.RETIREMENT,
            target_amount=100000.00,
            accumulated_amount=25000.00,
            start_date=datetime(2024, 1, 1),
            end_date=datetime(2034, 1, 1)
        )

        self.stdout.write(self.style.SUCCESS(
            'Test data successfully created!'))
