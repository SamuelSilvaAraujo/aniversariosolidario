from django.shortcuts import render

def index(request):
    return render(request, 'webapp/index.html')

def styleguide(request):
    return render(request, 'webapp/styleguide.html')