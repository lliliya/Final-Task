from django.contrib import admin
from .models import Ad, Category, Reply, User


class AdAdmin(admin.ModelAdmin):
    list_display = ('user', 'datetime_creation', 'header', 'text', 'category')
    list_filter = ('user', 'datetime_creation', 'category')
    search_fields = ('user', 'category')


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name']


class ReplyAdmin(admin.ModelAdmin):
    list_display = ('user', 'reply_text', 'ad')
    list_filter = ('user', 'ad')
    search_fields = ('user', 'ad')


admin.site.register(Ad, AdAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Reply, ReplyAdmin)
admin.site.register(User)
