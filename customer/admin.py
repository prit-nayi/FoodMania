from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Customer
from .models import Order
# Register your models here.

admin.site.register(Customer)
admin.site.register(Order)
