from django.contrib import admin
from .models import Rentor, ItemType, Item, CreditCard

"""Minimal registration of Models.
admin.site.register(Item)
admin.site.register(Rentor)
admin.site.register(ItemType)
admin.site.register(CreditCard)
"""

admin.site.register(ItemType)
admin.site.register(CreditCard)


class ItemsInline(admin.TabularInline):
    """Defines format of inline item insertion (used in Rentor Admin)"""
    model = Item


class RentorAdmin(admin.ModelAdmin):
    """Administration object for Rentor models.
    Defines:
     - fields to be displayed in list view (list_display)
     - orders fields in detail view (fields),
       grouping the date fields horizontally
     - adds inline addition of items in rentor view (inlines)
    """
    list_display = ('last_name',
                    'first_name', 'date_of_birth')
    fields = ['first_name', 'last_name', 'date_of_birth']
    inlines = [ItemsInline]

class CreditCardAdmin(admin.ModelAdmin):
    list_display = ('cc_number','cc_expiry','cc_code')
    fields = ['cc_number','cc_expiry','cc_code']

    model = CreditCard


class ItemAdmin(admin.ModelAdmin):
    """Administration object for Item models.
    Defines:
     - fields to be displayed in list view (list_display)
     - adds inline addition of item instances in item view (inlines)
    """
    list_display = ('title', 'rentor', 'display_item_type')


admin.site.register(Item, ItemAdmin)
