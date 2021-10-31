from django.urls import path

from .views import *

app_name = 'ab'


urlpatterns = [path('', index, name='index'),  # /ab/
               path('<int:abonent_id>/', one_person,
                    name='one person'),  # /ab/5
               ]
