import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "safecollab.settings")
from django.conf import settings

from django.contrib.auth.models import User
from users.models import UserProfile

u = User(username='admin')
u.set_password('admin')
u.first_name = 'The'
u.last_name = 'Admin'
u.is_superuser = True
u.is_staff = True
u.save()

p = UserProfile()
p.user = u
p.save()