from django.contrib import admin

from bot.models import TgUser

admin.site.register(TgUser)

# from django.contrib import admin
#
# from bot.models import TgUser
#
#
# @admin.register(TgUser)
# class TgUserAdmin(admin.ModelAdmin):
#     list_display = ('tg_chat_id', 'tg_username', 'user')
#     readonly_fields = ('tg_chat_id', 'verification_code')
