from django.shortcuts import redirect,render
from django.http import HttpRequest  
from django.contrib import messages  
from .models import Cart, CartItem, Product  

def view_cart(request: HttpRequest):
   pass
def add_to_cart(request: HttpRequest, product_id: int):
   pass
def remove_from_cart(request: HttpRequest, item_id: int):
    pass