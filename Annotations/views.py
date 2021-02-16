from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
import os

def index(request):
    return render(request, 'index.html')

def images(request):
    
    path="/home/aefuente/Annotations/Annotations/static/images/"

    img_list = os.listdir(path)



    return  render(request, 'images.html', {'images': img_list})
