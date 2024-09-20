from django.urls import re_path
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('expenses', views.ExpenseViewSet, basename='expenses')
router.register('incomes', views.IncomeViewSet, basename='incomes')
router.register('saving_goals', views.SavingGoalViewSet,
                basename='saving_goals')

urlpatterns = [
    re_path('login', views.login),
    re_path('register', views.register),
    re_path('logout', views.logout),
    re_path('cards', views.card_data),
]

urlpatterns += router.urls
