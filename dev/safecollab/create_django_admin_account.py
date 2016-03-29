import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "safecollab.settings")
from django.conf import settings

from django.contrib.auth.models import User

u = User(username='admin')
u.set_password('admin')
u.is_superuser = True
u.is_staff = True
u.save()