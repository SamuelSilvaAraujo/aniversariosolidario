from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required
def index(request):
    return render(request, 'webapp/index.html')

def styleguide(request):
    return render(request, 'webapp/styleguide.html')