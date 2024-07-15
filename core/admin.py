# core/admin.py

from django.contrib import admin
from .models import *

admin.site.register(CustomUsers)
admin.site.register(PDLocation)
# admin.site.register(DropLocation)
