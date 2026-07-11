from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from shop.models import Product
from .models import CartItem, Order, OrderItem
from .forms import OrderForm


@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    item, created = CartItem.objects.get_or_create(
        user=request.user,
        product=product
    )

    if not created:
        item.quantity += 1
        item.save()

    return redirect('cart_detail')


@login_required
def cart_detail(request):
    items = CartItem.objects.filter(user=request.user)

    total = 0
    for item in items:
        total += item.total_price()
    return render(request, 'cart/cart.html', {
        'items': items,
        'total': total
    })


@login_required
def remove_from_cart(request, item_id):
    item = get_object_or_404(CartItem, id=item_id, user=request.user)
    item.delete()
    return redirect('cart_detail')


@login_required
def place_order(request):
    form = OrderForm()
    items = CartItem.objects.filter(user=request.user)

    if request.method == 'POST':
        form = OrderForm(request.POST)

        if form.is_valid():
            order = Order.objects.create(
                user=request.user,
                phone=form.cleaned_data['phone'],
                address=form.cleaned_data['address']
            )

            for item in items:
                OrderItem.objects.create(
                    order=order,
                    product=item.product,
                    quantity=item.quantity
                )

            items.delete()

            return redirect('my_orders')

    return render(request, 'cart/place_order.html', {
        'form': form,
        'items': items
    })

@login_required
def increase_quantity(request, item_id):
    item = get_object_or_404(CartItem, id=item_id, user=request.user)
    item.quantity += 1
    item.save()
    return redirect('cart_detail')

@login_required
def decrease_quantity(request, item_id):
    item = get_object_or_404(CartItem, id=item_id, user=request.user)

    if item.quantity > 1:
        item.quantity -= 1
        item.save()
    else:
        item.delete()

    return redirect('cart_detail')

@login_required
def my_orders(request):
    orders = Order.objects.filter(
        user=request.user
    ).order_by('-id')

    return render(request, 'cart/my_orders.html', {
        'orders': orders
    })

@login_required
def order_detail(request, order_id):
    order = get_object_or_404(
        Order,
        id=order_id,
        user=request.user
    )

    items = OrderItem.objects.filter(order=order)

    total = order.total_price()

    return render(request, 'cart/order_detail.html', {
        'order': order,
        'items': items,
        'total': total,
    })
