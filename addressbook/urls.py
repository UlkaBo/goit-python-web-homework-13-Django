from django.contrib import admin
from django.urls import path, include
print('into addressbook/urls')
urlpattern = [path('finance/', include('finance.urls')),
              path('admin/', admin.site.urls), ]
