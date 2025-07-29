# products/urls.py
from django.urls import path
from .views import product_list


app_name = 'products'  # ✅ 加這一行，註冊 namespace

urlpatterns = [
    path('', product_list, name='product_list'),
]

