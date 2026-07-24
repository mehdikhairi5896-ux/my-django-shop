import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

if not User.objects.filter(username="Admin2").exists():
    User.objects.create_superuser(
        username="Admin2",
        email="admin2@example.com",
        password="1m2f3kh4b"
    )
    print("Admin created")
else:
    print("Admin already exists")
