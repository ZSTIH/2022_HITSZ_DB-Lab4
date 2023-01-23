from django.contrib import admin

from .models import Activity, Location, ActivityType

admin.site.register(Activity)
admin.site.register(Location)
admin.site.register(ActivityType)
