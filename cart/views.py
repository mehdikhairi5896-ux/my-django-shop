from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from shop.models import Product
from shop.models import Product
from .models import CartItem, Order, OrderItem, OrderPayment
from .forms import OrderForm
from django.db import transaction
from django.utils import timezone
from ads.payment import create_payment, verify_payment

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
    items = CartItem.objects.filter(user=request.user)

    if not items.exists():
        return redirect('cart_detail')

    form = OrderForm()

    if request.method == 'POST':
        form = OrderForm(request.POST)

        if form.is_valid():
            with transaction.atomic():
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
def pay_order(request, order_id):
    order = get_object_or_404(
        Order,
        id=order_id,
        user=request.user
    )

    # اگر سفارش قبلاً پرداخت موفق داشته باشد
    if OrderPayment.objects.filter(
        order=order,
        status="success"
    ).exists():
        return render(
            request,
            "cart/order_success.html",
            {
                "success": True,
                "order": order,
                "already_paid": True,
            }
        )

    if request.method == "POST":
        callback_url = request.build_absolute_uri(
            "/cart/payment/verify/"
        )

        result = create_payment(
            amount=order.total_price(),
            description=f"پرداخت سفارش {order.id}",
            callback_url=callback_url,
        )

        if result["success"]:
            payment = OrderPayment.objects.create(
                order=order,
                user=request.user,
                amount=order.total_price(),
                status="pending",
                authority=result["authority"],
            )

            return redirect(result["url"])

        return render(
            request,
            "cart/pay_order.html",
            {
                "order": order,
                "error": result["message"],
            }
        )

    return render(
        request,
        "cart/pay_order.html",
        {"order": order}
    )

@login_required
def test_order_payment(request, order_id):
    order = get_object_or_404(
        Order,
        id=order_id,
        user=request.user
    )

    # اگر سفارش قبلاً پرداخت موفق داشته باشد
    if OrderPayment.objects.filter(
        order=order,
        status="success"
    ).exists():
        return render(
            request,
            "cart/order_success.html",
            {
                "success": True,
                "order": order,
                "test_payment": True,
                "already_paid": True,
            }
        )

    if request.method == "POST":

        # جلوگیری از ایجاد پرداخت تستی تکراری
        if OrderPayment.objects.filter(
            order=order,
            status="success"
        ).exists():
            return render(
                request,
                "cart/order_success.html",
                {
                    "success": True,
                    "order": order,
                    "test_payment": True,
                    "already_paid": True,
                }
            )

        OrderPayment.objects.create(
            order=order,
            user=request.user,
            amount=order.total_price(),
            status="success",
            authority="TEST",
            ref_id="TEST",
            paid_at=timezone.now(),
        )
        order.status = "processing"
        order.save(update_fields=["status"])

        return render(
            request,
            "cart/order_success.html",
            {
                "success": True,
                "order": order,
                "test_payment": True,
            }
        )

    return render(
        request,
        "cart/pay_order.html",
        {
            "order": order,
            "test_payment": True,
        }
    )

@login_required
def verify_order_payment(request):
    authority = request.GET.get("Authority")
    status = request.GET.get("Status")

    if status != "OK" or not authority:
        return render(
            request,
            "cart/order_success.html",
            {"success": False}
        )

    payment = get_object_or_404(
        OrderPayment,
        authority=authority,
        user=request.user
    )

    if payment.status == "success":
        return render(
            request,
            "cart/order_success.html",
            {
                "success": True,
                "order": payment.order,
            }
        )

    result = verify_payment(
        payment.amount,
        authority
    )

    if "data" in result and result["data"].get("code") in [100, 101]:
        payment.status = "success"
        payment.ref_id = str(
            result["data"].get("ref_id", "")
        )
        payment.paid_at = timezone.now()
        payment.save()
        payment.order.status = "processing"
        payment.order.save(update_fields=["status"])

        return render(
            request,
            "cart/order_success.html",
            {
                "success": True,
                "order": payment.order,
            }
        )

    payment.status = "failed"
    payment.save(update_fields=["status"])

    return render(
        request,
        "cart/order_success.html",
        {"success": False}
    )

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

    for order in orders:
        order.is_paid = order.payments.filter(status="success").exists()

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
