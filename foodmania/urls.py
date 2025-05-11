"""
URL configuration for foodmania project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from customer import views 
from restaurant import views as rest
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.index, name='index'),
    path('food/<int:food_id>/', views.food_detail, name='food_detail'),
    path('restaurant/<int:restaurant_id>/', views.restaurant_detail, name='restaurant_detail'),
    path('login/',views.login, name='login'),
    path('logout/',views.logout, name='logout'),
    path('signup/',views.signup, name='signup'),
    path('profile/',views.profile, name='profile'),
    path('about-us/',views.aboutus, name='aboutus'),
    path('restaurant/registration',rest.registration, name='registration'),
    path('restaurant/dashboard',rest.dashboard, name='dashboard'),
    path('restaurant/login',rest.rest_login, name='rest_login'),
    path('restaurant/logout',rest.rest_logout, name='rest_logout'),
    path('restaurant/dashboard/menu',rest.menu, name='menu'),
    path('restaurant/dashboard/profile',rest.rest_profile, name='rest_profile'),
    path('cart/add/<int:food_id>', views.cart_add, name='cart_add'),
    path('cart/remove/<int:food_id>/', views.cart_remove, name='cart_remove'),
    path('cart/', views.cart_detail, name='cart_detail'),
    path('cart/', views.cart_detail, name='cart_detail'),
    path('payment/', views.payment, name='payment'),
    path('payment/process/', views.process_payment, name='process_payment'),
    path('order/success/<int:order_id>/', views.order_success, name='order_success'),
    path('orders/', rest.restaurant_orders, name='restaurant_orders'),
    path('bill/<int:order_id>/', views.download_bill, name='download_bill'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)




