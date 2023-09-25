from _decimal import Decimal

import pyotp
from django.shortcuts import render, redirect,HttpResponse
from app.models import Category,Product,Contact_US,Order
from django.contrib.auth import authenticate,login
from app.forms import UserCreateFrom
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from cart.cart import Cart
from django.contrib.auth.decorators import login_required



def Master(request):
    return render(request,'master.html')

# E_Shop/views.py
from django.core.mail import send_mail

import random
from django.conf import settings


def otp_login(request):
    if request.method == 'POST':
        # Generate a random OTP (6-digit)
        otp = ''.join([str(random.randint(0, 9)) for _ in range(6)])

        # Get the user's email from the form input
        email = request.POST.get('email')

        # Send the OTP to the user's email
        subject = 'Your OTP for Login'
        message = f'Your OTP for login: {otp}'
        from_email = settings.EMAIL_HOST_USER
        recipient_list = [email]

        try:
            send_mail(subject, message, from_email, recipient_list)
        except Exception as e:
            return HttpResponse("Error sending OTP email")

        # Store the OTP and email in the user's session
        request.session['otp'] = otp
        request.session['target_email'] = email

        # Redirect to OTP verification page
        return redirect('otp_verify')

    # Render the OTP login form
    return render(request, 'otp_login.html')

def otp_verify(request):
    if request.method == 'POST':
        entered_otp = request.POST.get('otp')
        stored_otp = request.session.get('otp')
        target_email = request.session.get('target_email')

        if entered_otp == stored_otp:
            # OTP is correct, log in the user
            # You can implement your login logic here
            # For example, authenticate the user and set the user session
            # Once logged in, you can redirect the user to the desired page
            return redirect('login')  # Redirect to the login page

        else:
            return HttpResponse("Invalid OTP. Please try again.")

    # Render the OTP verification form
    return render(request, 'otp_verify.html')





def Index(request):
    category=Category.objects.all()
    product=Product.objects.all()
    categoryID=request.GET.get('category')
    if categoryID:
        product=Product.objects.filter(sub_category=categoryID).order_by('-id')
    else:
        product = Product.objects.all()
    context={
        'category':category,
        'product':product
    }
    return render(request,'index.html',context)

def signup(request):
    global context

    if request.method=='POST':
        form=UserCreateFrom(request.POST)
        if form.is_valid():
            new_user=form.save()
            new_user=authenticate(
                username=form.cleaned_data['username'],
                password = form.cleaned_data['password1']

            )
            login(request,new_user)
            return redirect('index')

    else:
        form = UserCreateFrom()
        context = {
            'form': form,
            'redirect_msg': 'If You Face Redirection After your Signup then Email Already In Use',
        }
    return render(request,'registration/signup.html',context)

def cart_add(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.add(product=product)
    return redirect("index")



def item_clear(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.remove(product)
    return redirect("cart_detail")



def item_increment(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.add(product=product)
    return redirect("cart_detail")



def item_decrement(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.decrement(product=product)
    return redirect("cart_detail")



def cart_clear(request):
    cart = Cart(request)
    cart.clear()
    return redirect("cart_detail")



def cart_detail(request):
    cart = Cart(request)
    context = {
        'cart': cart,  # Pass the cart object to the template
    }
    return render(request, 'cart/cart_detail.html', context)


def Contact_Page(request):
    if request.method=='POST':
        contact=Contact_US(
            name=request.POST.get('name'),
            email=request.POST.get('email'),
            subject=request.POST.get('subject'),
            message=request.POST.get('message'),

        )
        contact.save()
    return render(request,'contact.html')


def Checkout(request):
    if request.method == 'POST':
        address=request.POST.get('address')
        phone = request.POST.get('phone')
        pincode = request.POST.get('pincode')
        cart=request.session.get('cart')
        uid=request.session.get('_auth_user_id')
        user=User.objects.get(pk=uid)
        for i in cart:
            a=int(cart[i]['price'])
            b=int(cart[i]['quantity'])
            total=a*b
            order=Order(
                user=user,
                product=cart[i]['name'],
                price=cart[i]['price'],
                quantity=cart[i]['quantity'],
                image=cart[i]['image'],
                address=address,
                phone=phone,
                pincode=pincode,
                total=total
            )
            order.save()
        request.session['cart']={}
        return redirect('index')
    #print(address,phone,pincode,cart,user)


def Your_Order(request):
    uid = request.session.get('_auth_user_id')
    user = User.objects.get(pk=uid)
    order=Order.objects.filter(user=user)
    cart_total_amount = sum(Decimal(item.total) for item in order)
    context ={
        'order':order,
        'cart_total_amount': cart_total_amount,
    }
    return render(request,'order.html',context)




# views.py





# views.py