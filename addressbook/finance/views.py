#! /usr/bin/env python3
"""Handlers for app finance
"""
from django.shortcuts import render, redirect, get_list_or_404
from django.utils import timezone
from django.urls import reverse
from django.views import generic
#from django.http import HttpResponseRedirect
from django.db.models import Sum

from .models import Transaction, Category


class IndexView(generic.ListView):
    """ Handler for index page of finance-app.Show all transactions."""
    model = Transaction
    template_name = "finance/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['sum_total'] = context['object_list'].aggregate(Sum('money'))
        return context


def report_filter(request, date_begin='0001-01-01', date_end=timezone.now()):
    """Show all transaction for period """

    if request.method == "POST":
        date_begin = request.POST.get('date_begin') or date_begin
        date_end = request.POST.get('date_end') or date_end

    transactions = Transaction.objects.filter(
        date__range=[date_begin, date_end]).order_by('-date')
    sum_total = transactions.aggregate(Sum('money'))
    result = {"transactions": transactions,
              'sum': sum_total['money__sum'],
              'date_begin': date_begin,
              'date_end': date_end,
              }
    return render(request, 'finance/report-filter.html', {'result': result})


def data_input(request):
    '''Show form for create new transaction. '''
    parameters = {}
    categories = get_list_or_404(Category, **parameters)
    if request.method == 'POST':
        transact = request.POST

        if transact and transact['money']:

            category = transact['category']

            category_obj = Category.objects.get(category_name=category)

            category_obj.transaction_set.create(money=transact['money'],
                                                date=transact['date'] or timezone.now(
            ), comment=transact['comment'])

        return redirect(reverse('finance:data-input'))
    transactions = Transaction.objects.all().order_by('-date')

    sum_total = Transaction.objects.aggregate(Sum('money'))

    result = {'categories': categories,
              'transactions': transactions,
              'sum': sum_total['money__sum'], }

    return render(request, 'finance/data-input.html', {'result': result})
