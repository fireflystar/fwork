from django.contrib import admin
from blog import models
# Register your models here.


class blogAdmin(admin.ModelAdmin):
    list_display = ('content', 'writer','ctime', 'uptime')
    search_fields = ('content', 'writer','ctime', 'uptime')
    ordering = ('-ctime',)

admin.site.register(models.blog, blogAdmin)

