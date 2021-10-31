#! /usr/bin/env python3
"""Urls for app finance
"""

from django.urls import path
from . import views

# pylint: disable=C0103
app_name = 'finance'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('data-input/', views.data_input, name='data-input'),
    path('report-filter/', views.report_filter, name='report-filter')]  # <data_begin>-<data_end>
