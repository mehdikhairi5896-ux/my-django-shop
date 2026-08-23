from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from datetime import timedelta

from .models import Advertisement, Payment
from .forms import AdvertisementForm
from .payment import create_payment

def ad_list(request):
    now = timezone.now()

    ads = Advertisement.objects.filter(
        paid=True,
        approved=True
    ).order_by("-created_at")

    active_ads = []

    for ad in ads:
        expire_date = ad.created_at + timedelta(days=ad.duration)

        if expire_date > now:
            active_ads.append(ad)

    return render(
        request,
        "ads/ad_list.html",
        {"ads": active_ads}
    )

def ad_detail(request, ad_id):
    ad = get_object_or_404(
        Advertisement,
        id=ad_id
    )

    return render(
        request,
        "ads/ad_detail.html",
        {"ad": ad}
    )

@login_required
def ad_create(request):
    if request.method == "POST":
        form = AdvertisementForm(
            request.POST,
            request.FILES
        )

        if form.is_valid():
            ad = form.save(commit=False)
            ad.owner = request.user
            ad.save()

            return redirect("ad_detail", ad_id=ad.id)

    else:
        form = AdvertisementForm()

    return render(
        request,
        "ads/ad_form.html",
        {"form": form}
    )

@login_required
def ad_edit(request, ad_id):
    ad = get_object_or_404(
        Advertisement,
        id=ad_id,
        owner=request.user
    )

    if request.method == "POST":
        form = AdvertisementForm(
            request.POST,
            request.FILES,
            instance=ad
        )

        if form.is_valid():
            ad = form.save(commit=False)
            ad.price = ad.get_price()
            ad.save()

            return redirect(
                "ad_detail",
                ad_id=ad.id
            )

    else:
        form = AdvertisementForm(
            instance=ad
        )

    return render(
        request,
        "ads/ad_form.html",
        {"form": form}
    )

@login_required
def ad_delete(request, ad_id):
    ad = get_object_or_404(
        Advertisement,
        id=ad_id,
        owner=request.user
    )

    if request.method == "POST":
        ad.delete()
        return redirect("ad_list")

    return render(
        request,
        "ads/ad_delete.html",
        {"ad": ad}
    )

@login_required
def pay_ad(request, ad_id):
    ad = get_object_or_404(
        Advertisement,
        id=ad_id,
        owner=request.user
    )

    if request.method == "POST":
        callback_url = request.build_absolute_uri(
            "/ads/verify/"
        )

        result = create_payment(
            amount=ad.get_price(),
            description=f"پرداخت آگهی: {ad.title}",
            callback_url=callback_url,
        )

        if result["success"]:
            payment = Payment.objects.create(
                advertisement=ad,
                user=request.user,
                amount=ad.get_price(),
                status="pending",
                authority=result["authority"],
            )

            return redirect(result["url"])

        return render(
            request,
            "ads/pay.html",
            {
                "ad": ad,
                "error": result["message"],
            }
        )

    return render(
        request,
        "ads/pay.html",
        {"ad": ad}
    )

@login_required
def test_payment(request, ad_id):
    ad = get_object_or_404(
        Advertisement,
        id=ad_id,
        owner=request.user
    )

    if request.method == "POST":
        payment = Payment.objects.create(
            advertisement=ad,
            user=request.user,
            amount=ad.get_price(),
            status="success",
            authority="TEST",
            ref_id="TEST",
            paid_at=timezone.now(),
        )

        ad.paid = True
        ad.approved = True
        ad.save(update_fields=["paid", "approved"])

        return render(
            request,
            "ads/success.html",
            {
                "success": True,
                "ad": ad,
                "test_payment": True,
            }
        )

    return render(
        request,
        "ads/pay.html",
        {
            "ad": ad,
            "test_payment": True,
        }
    )

@login_required
def verify_payment(request):
    authority = request.GET.get("Authority")
    status = request.GET.get("Status")

    if status != "OK" or not authority:
        return render(
            request,
            "ads/success.html",
            {"success": False}
        )

    payment = get_object_or_404(
        Payment,
        authority=authority,
        user=request.user
    )

    payment.status = "success"
    payment.ref_id = request.GET.get("RefID")
    payment.paid_at = timezone.now()
    payment.save()

    ad = payment.advertisement
    ad.paid = True
    ad.approved = True
    ad.save(update_fields=["paid", "approved"])

    return render(
        request,
        "ads/success.html",
        {"success": True, "ad": ad}
    )
