from django.shortcuts import render, get_list_or_404
from django.utils import timezone
from django.urls import reverse
from django.views import generic
from django.http import HttpResponseRedirect
from django.db.models import Sum

from .models import Transaction, Category


class IndexView(generic.ListView):
    model = Transaction
    template_name = "finance/index.html"


def report_filter(request, date_begin=None, date_end=None):
    if request.method == "POST":
        date_begin = request.POST.get('date_begin') or '0001-01-01'
        date_end = request.POST.get('date_end') or timezone.now()

    transactions = Transaction.objects.filter(
        date__range=[date_begin, date_end]).order_by('-date')
    print(transactions)
    sum = transactions.aggregate(Sum('money'))
    result = {"transactions": transactions,
              'sum': sum['money__sum'],
              'date_begin': date_begin,
              'date_end': date_end,
              }
    return render(request, 'finance/report-filter.html', {'result': result})


def data_input(request):
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

    transactions = Transaction.objects.all().order_by('-date')
    sum = Transaction.objects.aggregate(Sum('money'))

    result = {'categories': categories,
              'transactions': transactions,
              'sum': sum['money__sum'], }

    return render(request, 'finance/data-input.html', {'result': result})
