"""project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.urls import include
from login import views as login_views
from django.shortcuts import render

from django.conf.urls.static import static
from django.conf import settings
from cart import views as cart_views


urlpatterns = [
    path('admin/', admin.site.urls),
    
    path('', login_views.index, name='index'),  
    path('login/', login_views.login),
    path('register/', login_views.register),
    path('logout/', login_views.logout),

    path('accounts/', include('allauth.urls')),
    path('cart/', include('cart.urls')),
    path('products/', include('products.urls')),

    path('cart/remove/<int:product_id>/', cart_views.cart_remove, name='cart_remove'), # remove from cart

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)





# urlpatterns = [
#     path('admin/', admin.site.urls),
#     path('',login_views.index),
#     path('login/',login_views.login),
#     path('register/',login_views.register),
#     path('logout/',login_views.logout),

#     # Add Oath,根據ChatGPT修改
#     path('accounts/', include('allauth.urls')),
#     ## Add Cart購物車- 2025-0727,urls對應 cart的urls
#     path('cart/', include('cart.urls')),
#     path('products/', include('products.urls')),
#     ## 新增 Index
#     path('', lambda request: render(request, 'index.html'), name='home'),

# ]
