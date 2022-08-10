from django.contrib import admin

from .models import Application


class ApplicationAdmin(admin.ModelAdmin):
    list_display = ("id", "user_id", "value")


admin.site.register(Application, ApplicationAdmin)
