from django.contrib import admin
from django.urls import path, include
print('into addressbook/urls')
urlpattern = [
    path('admin/', admin.site.urls),
    path('auth/', include('user.urls', namespace='auth'), name='auth'),
    path('finance/', include('finance.urls', namespace='finance'), name='finance'),
    path('ab/', include('ab.urls', namespace='ab'), name='ab'),
]
