from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from .forms import MarketItemForm
from .models import MarketItem, MarketOrder


def market_list(request):
    items = MarketItem.objects.filter(
        is_active=True
    ).order_by("-created_at")

    return render(
        request,
        "market/market_list.html",
        {"items": items}
    )


@login_required
def market_detail(request, item_id):
    item = get_object_or_404(
        MarketItem,
        id=item_id,
        is_active=True
    )

    return render(
        request,
        "market/market_detail.html",
        {"item": item}
    )


@login_required
def market_buy(request, item_id):
    item = get_object_or_404(
        MarketItem,
        id=item_id,
        is_active=True
    )

    if item.owner == request.user:
        return redirect("market_detail", item_id=item.id)

    if request.method == "POST":
        MarketOrder.objects.create(
            buyer=request.user,
            item=item,
            price=item.price,
            status="pending"
        )

        return redirect("market_list")

    return render(
        request,
        "market/market_buy.html",
        {"item": item}
    )


@login_required
def market_create(request):

    if request.method == "POST":
        form = MarketItemForm(
            request.POST,
            request.FILES
        )

        if form.is_valid():
            item = form.save(commit=False)
            item.owner = request.user
            item.save()

            return redirect("market_detail", item_id=item.id)

    else:
        form = MarketItemForm()

    return render(
        request,
        "market/market_form.html",
        {"form": form}
    )
