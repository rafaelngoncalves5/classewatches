from django.shortcuts import render
from .models import Produto

# Create your views here.
def index(request):
    return render(request, 'lojarelogiosapp/index.html')

def products(request):
    return render(request, 'lojarelogiosapp/products.html', {'produtos': Produto.objects.all()})