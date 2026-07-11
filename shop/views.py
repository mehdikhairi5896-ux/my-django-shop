from django.shortcuts import render
from .models import Product

def shop(request):
    search = request.GET.get('search')

    if search:
        products = Product.objects.filter(name__icontains=search)
    else:
        products = Product.objects.all()

    return render(request, 'shop.html', {
        'products': products,
        'search': search,
    })
