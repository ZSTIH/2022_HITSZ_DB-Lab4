from django.contrib import admin

from .models import User, Organization, Department, ServiceEvaluation

admin.site.register(User)
admin.site.register(Organization)
admin.site.register(Department)
admin.site.register(ServiceEvaluation)
