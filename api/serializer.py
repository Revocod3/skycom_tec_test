from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Expense, Income, SavingGoal


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'email']
        extra_kwargs = {'password': {'write_only': True, 'required': True}}


class ExpenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expense
        fields = ['id', 'expense_type', 'amount', 'date', 'description']


class IncomeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Income
        fields = ['id', 'income_type', 'amount', 'date', 'description']


class SavingGoalSerializer(serializers.ModelSerializer):
    class Meta:
        model = SavingGoal
        fields = ['id', 'goal_type', 'target_amount',
                  'accumulated_amount', 'start_date', 'end_date']
