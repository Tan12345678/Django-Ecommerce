from django.contrib import admin

# Register your models here.
from .models import Category,Sub_Category,Product,Contact_US,Order,Brand
admin.site.register(Category)
admin.site.register(Sub_Category)
admin.site.register(Product)
admin.site.register(Contact_US)
admin.site.register(Order)
admin.site.register(Brand)
