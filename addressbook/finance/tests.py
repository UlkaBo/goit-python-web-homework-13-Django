#! /usr/bin/env python3
"""Tests for finance/view.py
"""
from decimal import Decimal
import datetime

from django.test import TestCase
from django.test.client import RequestFactory

from django.urls import reverse

from .models import Transaction, Category

from .views import IndexView, report_filter, data_input


class BaseFinanceTest(TestCase):
    '''Base test class  for views
    '''
    factory = RequestFactory()


class TestDataInputView(BaseFinanceTest):
    ''' test class  for view  data_input.
    '''

    def setUp(self):
        super().setUp()
        category = Category(category_name='test')
        category.save()
        self.path = reverse('finance:data-input')

    def tearDown(self):
        super().tearDown()
        Category.objects.all().delete()

    def test_get(self):
        '''test get data in page data_input
        '''
        response = self.client.get(self.path)

        self.assertEqual(response.status_code, 200)
        response_html = response.content.decode('utf-8')

        self.assertIn('money', response_html)
        self.assertIn('date', response_html)
        self.assertIn('category', response_html)
        self.assertIn('comment', response_html)

    def test_post(self):
        '''test post for date_input
        '''
        parameters = {
            'money': '444.00',
            'date': '2021-02-19',
            'category': 'test',
            'comment': 'test comment'
        }
        request = self.factory.post(self.path, parameters)
        transactions = Transaction.objects.all()
        data_input(request)
        self.assertEqual(Decimal(request.POST['money']), transactions[0].money)
        self.assertEqual(
            request.POST['category'], transactions[0].category.category_name)
        self.assertEqual(request.POST['date'], str(transactions[0].date))
        self.assertEqual(request.POST['comment'], transactions[0].comment)


class TestTransaction(BaseFinanceTest):
    '''test class for Transaction
    '''

    def setUp(self):
        category = Category(category_name='test')
        category.save()

    def tearDown(self):
        super().tearDown()
        Category.objects.all().delete()
        Transaction.objects.all().delete()

    def test_create(self):
        '''test create new record in Transaction
        '''
        category_obj = Category.objects.get(category_name='test')
        instance = category_obj.transaction_set.create(
            money=-1000,
            date=datetime.datetime(2021, 2, 2),
            comment='comment test')
        transaction = Transaction.objects.get(id=instance.id)
        check_date = datetime.date(2021, 2, 2)
        self.assertEqual(transaction.money, -1000)
        self.assertEqual(transaction.category.category_name, 'test')
        self.assertEqual(transaction.date,
                         check_date)
        self.assertEqual(transaction.comment, 'comment test')


class TestIndexPage(BaseFinanceTest):
    '''test class for view IndexView
    '''

    def setUp(self):
        self.path = reverse('finance:index')
        category = Category(category_name='test')
        category.save()
        category = Category(category_name='test for context')
        category.save()
        category_obj = Category.objects.get(category_name='test for context')
        category_obj.transaction_set.create(
            money=2000,
            date=datetime.datetime(2021, 2, 2),
            comment='comment test')

    def tearDown(self):
        super().tearDown()
        Category.objects.all().delete()
        Transaction.objects.all().delete()

    def test_get_context(self):
        '''test get context in index page
        '''

        request = self.factory.get(self.path)
        response = IndexView.as_view(model=Transaction)(request)
        context = response.context_data
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(context['object_list']), 1)
        self.assertEqual(context['sum_total']['money__sum'], Decimal(2000))


class TestReport(BaseFinanceTest):
    '''test class for view report_filter
    '''

    def setUp(self):
        self.path = reverse('finance:report-filter')
        self.instances_id = []
        super().setUp()
        category = Category(category_name='test')
        category.save()
        category_obj = Category.objects.get(category_name='test')
        instance = category_obj.transaction_set.create(
            money=2000,
            date=datetime.datetime(2021, 9, 2),
            comment='comment 2000')
        self.instances_id.append(instance.id)
        instance = category_obj.transaction_set.create(
            money=100,
            date=datetime.datetime(2021, 2, 2),
            comment='comment 100')
        self.instances_id.append(instance.id)

        category = Category(category_name='test for context')
        category.save()
        category_obj = Category.objects.get(category_name='test for context')
        instance = category_obj.transaction_set.create(
            money=-2000,
            date=datetime.datetime(2021, 10, 2),
            comment='comment -2000')
        self.instances_id.append(instance.id)
        instance = category_obj.transaction_set.create(
            money=-100,
            date=datetime.datetime(2021, 1, 20),
            comment='comment -100')
        self.instances_id.append(instance.id)

    def tearDown(self):
        super().tearDown()
        Category.objects.all().delete()
        Transaction.objects.all().delete()

    def test_report_get(self):
        '''test report_filter get
        '''

        date_begin, date_end = '2021-10-01', '2021-11-01'

        request = self.factory.get(self.path)

        response = report_filter(
            request, date_begin=date_begin, date_end=date_end)

        response_html = response.content.decode('utf-8')
        self.assertEqual(response.status_code, 200)
        self.assertIn('is -2000.00', response_html)

    def test_report_post(self):
        '''test report_filter post
        '''

        request = self.factory.post(self.path)
        response = report_filter(request)
        response_html = response.content.decode('utf-8')
        self.assertEqual(response.status_code, 200)
        self.assertIn('date_begin', response_html)
        self.assertIn('date_end', response_html)
