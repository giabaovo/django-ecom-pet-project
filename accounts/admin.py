from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html
from accounts.models import Account, UserProfile

class AccountAdmin(UserAdmin):
    list_display = ["first_name", "last_name", "username", "email"]

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ["thumbnail", "user", "full_address", "country", "state", "city"]

    def thumbnail(self, obj):
        return format_html('<img src="{}" width="30" style="border-radius:50%" />'.format(obj.profile_picture.url))

admin.site.register(Account, AccountAdmin)
admin.site.register(UserProfile, UserProfileAdmin)
