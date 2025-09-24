from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),  # 根目錄導向首頁
]
