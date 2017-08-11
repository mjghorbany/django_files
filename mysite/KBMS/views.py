from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic.edit import CreateView

from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request,'KBMS/home2.html')

def ontology(request):
    return render(request,'KBMS/home3.html')