from django.db import models
from django.contrib.auth.models import User
import datetime
from django.contrib.auth.password_validation import MinimumLengthValidator, CommonPasswordValidator

# app/models.py]


# Create your models here.
class Category(models.Model):
    name=models.CharField(max_length=200)

    def __str__(self):
        return self.name
class Sub_Category(models.Model):
    name=models.CharField(max_length=150)
    category=models.ForeignKey(Category,on_delete=models.CASCADE)

    def __str__(self):
        return self.name



class Brand(models.Model):
    name=models.CharField(max_length=200)
    def __str__(self):
        return self.name

class Product(models.Model):
    category=models.ForeignKey(Category,on_delete=models.CASCADE,null=False,default='')
    sub_category=models.ForeignKey(Sub_Category,on_delete=models.CASCADE,null=False,default='')
    brand=models.ForeignKey(Brand,on_delete=models.CASCADE,null=True)
    image=models.ImageField(upload_to='ecommerce/pimg')
    name=models.CharField(max_length=100)
    price=models.IntegerField()
    date=models.DateField(auto_now_add=True)

    def __str__(self):
        return self.name



class Contact_US(models.Model):
    name=models.CharField(max_length=100)
    email=models.EmailField(max_length=100)
    subject=models.CharField(max_length=100)
    message=models.TextField(max_length=100)
    def __str__(self):
        return self.name

class Order(models.Model):
    image=models.ImageField(upload_to='ecommerce/order/image')
    product=models.CharField(max_length=200,default='')
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    quantity=models.CharField(max_length=5)
    price=models.IntegerField()
    address=models.TextField()
    phone=models.CharField(max_length=10)
    pincode=models.CharField(max_length=10)
    total=models.CharField(max_length=200,default='')
    date=models.DateField(default=datetime.datetime.today)

    def __str__(self):
        return self.product

