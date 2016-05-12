from django.contrib import admin
from django.core import urlresolvers
from django.utils.html import format_html

from .models import Share, Quote


class ShareAdmin(admin.ModelAdmin):
    list_display = ('symbol', 'start', 'end')
admin.site.register(Share, ShareAdmin)


class QuoteAdmin(admin.ModelAdmin):
    list_display = ('id', 'share_link', 'date', 'open', 'close', 
                    'adj_close', 'low', 'high', 'volume')
    list_select_related = ('share',)
    
    def share_link(self, obj):
        url = urlresolvers.reverse('admin:collector_share_change', args=(obj.share_id,))
        return format_html('<a href="{}">{}</a>'.format(url, obj.share.symbol)) 
    
admin.site.register(Quote, QuoteAdmin)

