from django.shortcuts import render
from shop.models import Product

def home(request):
    return render(request, 'index.html', {'test_message': 'صفحه خانه درست است'})

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

def product_detail(request, product_id):
    product = Product.objects.get(id=product_id)
    return render(request, 'product_detail.html', {'product': product})
