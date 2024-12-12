from django.shortcuts import render
from django.http import HttpRequest
from autoparts.models import Category


# Create your views here.
def home_view(request: HttpRequest):
    categories = Category.objects.all()
    context = {"categories": categories}

    return render(request, "main/index.html", context)



def form_example(request: HttpRequest):

    return render(request, "main/form_example.html")



def content_example(request: HttpRequest):

    return render(request, "main/content_example.html")
