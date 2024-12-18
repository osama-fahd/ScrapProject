from django.shortcuts import render, redirect
from django.http import HttpRequest
from autoparts.models import Category
from django.contrib import messages
from .forms import ContactForm



# Create your views here.
def home_view(request: HttpRequest):
    categories = Category.objects.all()
    context = {"categories": categories}

    return render(request, "main/index.html", context)


def contact_view(request:HttpRequest):
    contact_form = ContactForm()
    
    if request.method == "POST":
        contact_form = ContactForm(request.POST)
        if contact_form.is_valid():
            contact_form.save()
            messages.success(request, "تم ارسال رسالتك بنجاح!", "alert-success")
            return redirect('main:home_view')
        else:
            messages.error(request, "حدث خطأ اثناء الارسال", "alert-danger")
            return render(request, "main/contact.html")

    return render(request, 'main/contact.html')


def form_example(request: HttpRequest):

    return render(request, "main/form_example.html")



def content_example(request: HttpRequest):

    return render(request, "main/content_example.html")
