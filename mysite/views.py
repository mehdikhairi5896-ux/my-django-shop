from django.shortcuts import render

def home(request):
    return render(request, 'index.html', {'test_message': 'صفحه خانه درست است'})

