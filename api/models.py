from django.db import models
from django.contrib.auth.models import User

# ExpenseType Enum


class ExpenseType(models.TextChoices):
    FOOD = 'FOOD', 'Food'
    TRANSPORT = 'TRANSPORT', 'Transport'
    ENTERTAINMENT = 'ENTERTAINMENT', 'Entertainment'
    BILLS = 'BILLS', 'Bills'
    OTHER = 'OTHER', 'Other'

# IncomeType Enum


class IncomeType(models.TextChoices):
    SALARY = 'SALARY', 'Salary'
    FREELANCE = 'FREELANCE', 'Freelance'
    INVESTMENT = 'INVESTMENT', 'Investment'
    GIFT = 'GIFT', 'Gift'
    OTHER = 'OTHER', 'Other'

# SavingGoalType Enum


class SavingGoalType(models.TextChoices):
    VACATION = 'VACATION', 'Vacation'
    EMERGENCY = 'EMERGENCY', 'Emergency'
    RETIREMENT = 'RETIREMENT', 'Retirement'
    PURCHASE = 'PURCHASE', 'Purchase'
    OTHER = 'OTHER', 'Other'


# Expense Model


class Expense(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    expense_type = models.CharField(max_length=20, choices=ExpenseType.choices)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f'Expense of {self.amount} by {self.user}'

# Income Model


class Income(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    income_type = models.CharField(max_length=20, choices=IncomeType.choices)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f'Income of {self.amount} by {self.user}'

# SavingGoal Model


class SavingGoal(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    goal_type = models.CharField(
        max_length=20, choices=SavingGoalType.choices)
    target_amount = models.DecimalField(max_digits=10, decimal_places=2)
    accumulated_amount = models.DecimalField(
        max_digits=10, decimal_places=2, default=0)
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return f'Saving goal of {self.target_amount} for {self.user}'
