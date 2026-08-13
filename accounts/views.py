from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import Profile
from .forms import ProfileForm
from cart.models import Order
from django.contrib.auth import login
from .forms import RegisterForm

@login_required
def profile_view(request):
    profile, created = Profile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
    else:
        form = ProfileForm(instance=profile)

    print("USER:", request.user.username)
    print("COUNT:", Order.objects.filter(user=request.user).count())

    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    order_count = orders.count()
    cart_count = request.user.cartitem_set.count()   
    orders_count = orders.count()

    return render(request, 'accounts/profile.html', {
        'form': form,
        'profile': profile,
        'orders': orders,
        'orders_count': orders_count,
        'order_count': order_count,
        'cart_count': cart_count, 
   })

def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data["password"])
            user.save()

            login(request, user)

            return redirect("home")
    else:
        form = RegisterForm()

    return render(request, "accounts/register.html", {"form": form})
