from django.db import models
from django.utils import timezone


class Category(models.Model):
    category_name = models.CharField(max_length=100)

    def __str__(self):
        return self.category_name


class Transaction(models.Model):
    money = models.DecimalField(default=0, max_digits=8, decimal_places=2)
    date = models.DateTimeField(default=timezone.now)
    comment = models.CharField(default='', max_length=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.date} {self.category} {self.money} {self.comment}'
