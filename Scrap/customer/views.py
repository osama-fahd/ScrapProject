from django.shortcuts import redirect, render
from django.http import HttpRequest, HttpResponse
from django.contrib import messages
from accounts.models import ProfileCustomer
from django.contrib.auth.models import User
from .models import Cart, CartItem ,Product


# Create your views here.


#@login_required

def view_cart(request:HttpRequest):
    pass

def add_to_cart(request:HttpRequest, product_id):
   pass


def remove_from_cart(request:HttpRequest, item_id):
    pass
