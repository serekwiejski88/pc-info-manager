from django.contrib import admin
from .models import Info, Process, Disk

# Register your models here.

admin.site.register(Info)
admin.site.register(Process)
admin.site.register(Disk)