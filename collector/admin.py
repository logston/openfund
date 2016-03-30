from django.contrib import admin

from .models import Share, Quote

class ShareAdmin(admin.ModelAdmin):
    pass
admin.site.register(Share, ShareAdmin)


class QuoteAdmin(admin.ModelAdmin):
    pass
admin.site.register(Quote, QuoteAdmin)

