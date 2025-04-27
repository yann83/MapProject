# floorproject/public/views.py
from django.shortcuts import render

def public_index(request):
    return render(request, 'public/index.html')

def public_plans(request):
    return render(request, 'public/plans.html')

def public_cartes(request):
    return render(request, 'public/cartes.html')