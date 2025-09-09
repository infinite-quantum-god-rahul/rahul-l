from django.contrib import admin
from .models import Users

@admin.register(Users)
class UsersAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "staff",
        "full_name",
        "branch",
        "department",
        "mobile",
        "status",
    )
    search_fields = ("user", "staff__name", "full_name", "branch__name")
    list_filter = ("status", "branch")
    list_select_related = ("staff", "branch")
