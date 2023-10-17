from django.shortcuts import render

# Create your views here.

def home_list(request):
    return render(request, 'servicios/home_list.html', {})