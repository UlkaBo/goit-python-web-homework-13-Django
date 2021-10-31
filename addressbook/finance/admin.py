#! /usr/bin/env python3
"""for access for admin panel
"""

from django.contrib import admin

from .models import Category

admin.site.register(Category)
