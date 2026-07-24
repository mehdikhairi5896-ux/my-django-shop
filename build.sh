#!/usr/bin/env bash
set -o errexit

python manage.py collectstatic --no-input

python manage.py migrate

python manage.py shell -c "
from django.contrib.auth.models import User

User.objects.filter(username='renderadmin').delete()

u = User.objects.create_superuser(
    username='renderadmin',
    email='renderadmin@example.com',
    password='12345678'
)

print('NEW ADMIN CREATED:', u.username)
"
