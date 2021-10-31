#! /usr/bin/env python3
"""Models for app finance
"""
from django.db import models


class Category(models.Model):
    ''' Types of transaction'''
    category_name = models.CharField(max_length=100)
    objects = models.Manager()

    def __str__(self):
        return str(self.category_name)


class Transaction(models.Model):
    ''' Transaction . '''
    money = models.DecimalField(default=0, max_digits=8, decimal_places=2)
    date = models.DateField()
    comment = models.CharField(default='', max_length=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    objects = models.Manager()

    def __str__(self):
        return f'{self.date} {self.category} {self.money} {self.comment}'
