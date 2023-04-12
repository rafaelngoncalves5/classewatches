from django.contrib import admin
from .models import Produto, Pedido, Carrinho

# Register your models here.
admin.site.register(Produto)
admin.site.register(Pedido)
admin.site.register(Carrinho)

'''
class ProdutoAdmin(admin.ModelAdmin):
    list_display = ('title', 'publisher', 'publication_date')
    list_filter = ('publication_date',)
    date_hierarchy = 'publication_date'
    ordering = ('-publication_date',)
    filter_horizontal = ('authors',)
    raw_id_fields = ('publisher',)
'''