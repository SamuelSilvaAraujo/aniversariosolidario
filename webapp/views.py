from django.shortcuts import render

def index(request):
    return render(request, 'webapp/index.html')

def styleguide(request):
    return render(request, 'webapp/styleguide.html')

def raisee(request):
    raise

def termos_uso(request):
    return render(request, 'webapp/termos_uso.html')