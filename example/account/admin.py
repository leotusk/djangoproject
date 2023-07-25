from django.contrib import admin
from .models import Account

# Register your models here.
@admin.register(Account)
class ShowAccount(admin.ModelAdmin):
    list_display=(
        'user_id',
        'user_pw',
        'user_name',
        'user_number',
        'user_register_dttm'
    )