from django.shortcuts import render,redirect
from django.http import HttpRequest, HttpResponse
# Create your views here.

def new_brand(request: HttpRequest):

    return render(request, "Vehicle/new_brand.html")