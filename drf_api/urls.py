from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path(
        'admin/',
        admin.site.urls
    ),
    path(
        'auth/',
        include('users.urls')
    ),
    path(
        'transactions/',
        include('transactions.urls')
    ),
    path(
        'categories/',
        include('categories.urls')
    ),
    path(
        'budgets/',
        include('budgets.urls')
    ),
    path(
        'reports/',
        include('reports.urls')
    ),
]
