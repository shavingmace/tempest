from django.contrib import admin
from .models import TempestUser as User

# Register your models here.

admin.site.register(User)