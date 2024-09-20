from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status, viewsets
from rest_framework.decorators import permission_classes, authentication_classes, action
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token

from api.utils import generate_csv, generate_pdf

from .serializer import IncomeSerializer, SavingGoalSerializer, UserSerializer, ExpenseSerializer
from .models import Expense, Income, SavingGoal
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.db.models import Sum, F
import numpy as np

# Create session


@api_view(['POST'])
def login(request):
    print(request.data)
    username = request.data.get('username')
    password = request.data.get('password')
    try:
        user = User.objects.get(username=username)
        if user.check_password(password):
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key, 'user': UserSerializer(user).data}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)
    except User.DoesNotExist:
        return Response({'error': 'User does not exist'}, status=status.HTTP_400_BAD_REQUEST)

# Create User


@api_view(['POST'])
def register(request):
    print(request.data)
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        user = User.objects.get(username=serializer.data['username'])
        user.set_password(request.data['password'])
        user.save()

        token = Token.objects.create(user=user)
        return Response({'token': token.key, 'user': serializer.data}, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Logout


@api_view(['POST'])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def logout(request):
    request.user.auth_token.delete()
    return Response('Logged out', status=status.HTTP_200_OK)

# Expenses Viewset


class ExpenseViewSet(viewsets.ModelViewSet):
    queryset = Expense.objects.all()
    serializer_class = ExpenseSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get_queryset(self):
        return Expense.objects.filter(user=self.request.user).order_by('-date')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=False, methods=['get'], url_path='summary')
    def expenses_summary(self, request):
        user = request.user
        today = timezone.now().date()

        # Daily expenses
        daily_expenses = Expense.objects.filter(
            user=user,
            date=today
        ).aggregate(total=Sum('amount'))['total'] or 0

        # Weekly expenses
        start_of_week = today - timezone.timedelta(days=today.weekday())
        end_of_week = start_of_week + timezone.timedelta(days=6)
        weekly_expenses = Expense.objects.filter(
            user=user,
            date__range=[start_of_week, end_of_week]
        ).aggregate(total=Sum('amount'))['total'] or 0

        # Monthly expenses
        start_of_month = today.replace(day=1)
        end_of_month = (start_of_month + timezone.timedelta(days=32)
                        ).replace(day=1) - timezone.timedelta(days=1)
        monthly_expenses = Expense.objects.filter(
            user=user,
            date__range=[start_of_month, end_of_month]
        ).aggregate(total=Sum('amount'))['total'] or 0

        return Response({
            'daily_expenses': daily_expenses,
            'weekly_expenses': weekly_expenses,
            'monthly_expenses': monthly_expenses,
        })

    @action(detail=False, methods=['get'], url_path='stats')
    def expenses_over_time(self, request):
        user = request.user
        month = request.query_params.get('month')
        year = request.query_params.get('year')

        expenses = Expense.objects.filter(user=user)

        if month and year:
            expenses = expenses.filter(date__year=year, date__month=month)
        elif year:
            expenses = expenses.filter(date__year=year)

        expenses = expenses.values('date').annotate(
            total=Sum('amount')).order_by('date')

        expenses_list = [
            {'date': expense['date'].strftime(
                '%b %d'), 'Gasto': expense['total']}
            for expense in expenses
        ]

        return Response(expenses_list)

    @action(detail=False, methods=['get'], url_path='by_type')
    def expenses_by_category(self, request):
        user = request.user
        expenses = Expense.objects.filter(user=user).values(
            'expense_type').annotate(total=Sum('amount')).order_by('expense_type')

        # Get all unique expense types from the database
        all_expense_types = Expense.objects.values_list(
            'expense_type', flat=True).distinct()

        expense_type_colors = {
            'FOOD': '#CB3234',
            'TRANSPORT': '#828282',
            'ENTERTAIMENT': '#F3A505',
            'BILLS': '#1D1E33',
            'OTHER': '#F75E25'
        }

        # Ensure all expense types are included in the response
        expenses_dict = {expense['expense_type']: expense['total'] for expense in expenses}
        expenses_list = [
            {
                'name': expense_type,
                'value': expenses_dict.get(expense_type, 0),
                'color': expense_type_colors.get(expense_type, '#3B83BD')
            }
            for expense_type in all_expense_types
        ]

        return Response(expenses_list)

    @action(detail=False, methods=['get'], url_path='report')
    def expense_report(self, request):
        user = request.user
        format = request.query_params.get('format', 'csv')

        expenses = Expense.objects.filter(user=user).values_list(
            'date', 'amount', 'expense_type', 'description'
        )

        data = {
            'headers': ['Date', 'Amount', 'Type', 'Description'],
            'rows': list(expenses)
        }

        if format == 'pdf':
            return generate_pdf(data, 'expenses_report')
        else:
            return generate_csv(data, 'expenses_report')

# Income Viewset


class IncomeViewSet(viewsets.ModelViewSet):
    queryset = Income.objects.all()
    serializer_class = IncomeSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get_queryset(self):
        return Income.objects.filter(user=self.request.user).order_by('-date')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=False, methods=['get'], url_path='by_type')
    def income_by_category(self, request):
        user = request.user
        incomes = Income.objects.filter(user=user).values(
            'income_type').annotate(total=Sum('amount')).order_by('income_type')

        # Get all unique income types from the database
        all_income_types = Income.objects.values_list(
            'income_type', flat=True).distinct()

        income_type_colors = {
            'SALARY': '#4CAF50',
            'FREELANCE': '#FFC107',
            'BUSINESS': '#FF9800',
            'INVESTMENT': '#2196F3',
            'OTHER': '#9C27B0'
        }

        incomes_dict = {income['income_type']: income['total']
                        for income in incomes}
        incomes_list = [
            {
                'name': income_type,
                'value': incomes_dict.get(income_type, 0),
                'color': income_type_colors.get(income_type, '#3B83BD')
            }
            for income_type in all_income_types
        ]

        return Response(incomes_list)

    @action(detail=False, methods=['get'], url_path='report')
    def income_report(self, request):
        user = request.user
        format = request.query_params.get('format', 'csv')

        incomes = Income.objects.filter(user=user).values_list(
            'date', 'amount', 'income_type', 'description'
        )

        data = {
            'headers': ['Date', 'Amount', 'Type', 'Description'],
            'rows': list(incomes)
        }

        if format == 'pdf':
            return generate_pdf(data, 'incomes_report')
        else:
            return generate_csv(data, 'incomes_report')
# SavingGoal Viewset


class SavingGoalViewSet(viewsets.ModelViewSet):
    queryset = SavingGoal.objects.all()
    serializer_class = SavingGoalSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get_queryset(self):
        return SavingGoal.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def card_data(request):
    user = request.user

    # Calculate total income
    total_income = Income.objects.filter(user=user).aggregate(
        total=Sum('amount'))['total'] or 0

    # Calculate total expenses
    total_expenses = Expense.objects.filter(
        user=user).aggregate(total=Sum('amount'))['total'] or 0

    # Calculate balance
    balance = total_income - total_expenses

    return Response({
        'total_income': total_income,
        'total_expenses': total_expenses,
        'balance': balance
    }, status=status.HTTP_200_OK)
