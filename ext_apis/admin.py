from django.contrib import admin
from .models import TransactionLog

from django.contrib import admin
from .models import TransactionLog


@admin.register(TransactionLog)
class TransactionLogAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'transaction_type',
        'transaction_status',
        'user',
        'shop',
        'profit',
        'date_created'
    )
    list_filter = (
        'transaction_type',
        'transaction_status',
        'date_created',
        'shop'
    )
    search_fields = (
        'user', 'shop', 'products',
        'mpesa_transaction_code',
        'receipt_ID',
        'customer_number',
        'user__username',
        'shop__branch_name'
    )
    readonly_fields = ('date_created',)
    fieldsets = (
        ("Transaction Details", {
            'fields': (
                'mpesa_transaction_code',
                'transaction_type',
                'transaction_status',
                'user',
                'shop',
                'receipt_ID',
                'customer_number'
            )
        }),
        ("Products & Profit", {
            'fields': (
                'products',
                'profit',
                'product_quantities'
            )
        }),
        ("Additional Info", {
            'fields': (
                'date_created',
            )
        }),
    )
    autocomplete_fields = ('user', 'shop', 'products')
    ordering = ('-date_created',)

    def get_queryset(self, request):
        """
        Customize queryset to prefetch related data for efficiency.
        """
        queryset = super().get_queryset(request)
        return queryset.select_related('user', 'shop').prefetch_related('products')
