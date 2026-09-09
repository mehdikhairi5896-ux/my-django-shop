#!/usr/bin/env bash
set -o errexit

python manage.py collectstatic --no-input

python manage.py migrate

python manage.py shell -c "

from django.contrib.auth.models import User
import os
User.objects.filter(username='renderadmin').delete()

u = User.objects.create_superuser(
    username='renderadmin',
    email='renderadmin@example.com',
    password=os.environ.get('RENDER_ADMIN_PASSWORD')
)

print('NEW ADMIN CREATED:', u.username)
"
