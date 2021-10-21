from django.urls import path

from . import views
print('into ab/urls')
urlpatterns = [path('', views.index, name='index'),  # /ab/
               path('<int:abonent_id>/', views.one_person,
                    name='one person'),  # /ab/5
               ]
