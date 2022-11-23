from django.contrib import admin
from core.models import User

class UserAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'username', 'email')
    list_display_links = ('last_name', 'first_name', 'username', 'email')
    search_fields = ('last_name', 'first_name', 'username', 'email')
    list_filter = ('is_staff', 'is_active', 'is_superuser')
    fields = ('username', 'first_name', 'last_name', 'email', 'is_staff', 'is_active',
              'date_joined', 'last_login')
    readonly_fields = ('date_joined', 'last_login')
    exclude = ('password',)


admin.site.register(User, UserAdmin)