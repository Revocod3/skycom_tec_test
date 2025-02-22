# Generated by Django 5.1.1 on 2024-09-18 18:15

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Expense',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('expense_type', models.CharField(choices=[('FOOD', 'Food'), ('TRANSPORT', 'Transport'), ('ENTERTAINMENT', 'Entertainment'), ('BILLS', 'Bills'), ('OTHER', 'Other')], max_length=20)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('date', models.DateField()),
                ('description', models.TextField(blank=True, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Income',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('income_type', models.CharField(choices=[('SALARY', 'Salary'), ('FREELANCE', 'Freelance'), ('INVESTMENT', 'Investment'), ('GIFT', 'Gift'), ('OTHER', 'Other')], max_length=20)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('date', models.DateField()),
                ('description', models.TextField(blank=True, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='SavingGoal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('saving_goal_type', models.CharField(choices=[('VACATION', 'Vacation'), ('EMERGENCY', 'Emergency'), ('RETIREMENT', 'Retirement'), ('PURCHASE', 'Purchase'), ('OTHER', 'Other')], max_length=20)),
                ('target_amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('accumulated_amount', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('start_date', models.DateField()),
                ('end_date', models.DateField(blank=True, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
