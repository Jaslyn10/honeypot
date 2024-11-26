from django.contrib import admin

# Register your models here.
from .models import UnauthorizedAccessLog,BlockedIP

admin.site.register(UnauthorizedAccessLog)
admin.site.register(BlockedIP)