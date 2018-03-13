from django.contrib import admin
from fisChannel import models
# Register your models here.

class tongdaoAdmin(admin.ModelAdmin):
    list_display = ('ip', 'tongdaoN','tongdaoFull', 'description',
                    'sheetName','instance','remarks','ctime','uptime',
                    'tongdao_type_id','sb_id')
    search_fields = ('ip', 'tongdaoN','tongdaoFull', 'description',
                    'sheetName','instance','remarks','ctime','uptime',
                    'tongdao_type_id')
    ordering = ('-ctime',)


class shebeiAdmin(admin.ModelAdmin):
    list_display = ('shebei_id', 'shebeiN','factory','department', 'shebeRemarks')
    search_fields = ('shebei_id', 'shebeiN','factory','department', 'shebeRemarks')
    ordering = ('-shebei_id',)



class contactAdmin(admin.ModelAdmin):
    list_display = ('contact_id', 'contacts','mobile', 'tel', 'email')
    search_fields = ('contact_id', 'contacts','mobile', 'tel')
    ordering = ('-contact_id',)

admin.site.register(models.tongdao, tongdaoAdmin)
admin.site.register(models.contact, contactAdmin)
admin.site.register(models.shebei, shebeiAdmin)