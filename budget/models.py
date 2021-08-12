from django.db import models
from accounts.models import User
from django.utils.timezone import now
from app.models import Facility


class IncomeCategory(models.Model):
    name = models.CharField(max_length=255, default="")

    def __str__(self):
        return self.name


class Income(models.Model):
    added_by = models.ForeignKey(
        User, on_delete=models.CASCADE, blank=True, null=True)
    amount = models.IntegerField(default=0)
    income_categories = [
        ('1', 'Аванс за мероприятия'),
        ('2', 'Довнесение'),
        ('3', 'Другое'),
    ]
    category = models.CharField(
        default='1', max_length=255, choices=income_categories)
    description = models.TextField(default="", max_length=1000)
    is_verified = models.BooleanField(default=False)
    contragent = models.CharField(max_length=255, default="")
    facility = models.ForeignKey(
        Facility, blank=True, null=True, default=None, on_delete=models.CASCADE)
    added_at = models.DateField(default=now)


class ExpenseCategory(models.Model):
    name = models.CharField(max_length=255, default="")

    def __str__(self):
        return self.name


class Expense(models.Model):
    added_by = models.ForeignKey(User, on_delete=models.CASCADE)
    added_at = models.DateField(default=now)
    amount = models.IntegerField(default=0)
    expense_categories = [
        ('1', 'Аванс'),
        ('2', 'Продукты'),
        ('3', 'Хозтовары'),
        ('4', 'Посуда'),
        ('5', 'Инкассация'),
        ('6', 'Под отчёт'),
        ('7', 'Реклама'),
        ('8', 'Ремонтные работы'),
        ('9', 'Другое'),
    ]
    category = models.CharField(
        default='1', max_length=255, choices=expense_categories)
    description = models.TextField(default="", max_length=1000)
    is_verified = models.BooleanField(default=False)
    contragent = models.CharField(max_length=255, default="")
    facility = models.ForeignKey(
        Facility, blank=True, null=True, default=None, on_delete=models.CASCADE)
