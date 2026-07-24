#!/usr/bin/env bash
set -o errexit

python manage.py collectstatic --no-input

python manage.py migrate

python manage.py shell -c "
from django.contrib.auth.models import User

u, created = User.objects.get_or_create(username='Admin2')

u.set_password('12345678')
u.is_staff = True
u.is_superuser = True
u.save()

print('Admin2 ready')
"
