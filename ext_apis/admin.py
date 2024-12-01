from django.contrib import admin
from .models import TransactionLog


class TransactionLogAdmin(admin.ModelAdmin):
    list_display = (
        'transaction_type',
        'user',
        'shop',
        'profit',
        'date_created',
        'customer_number',
        'receipt_ID',
        'transaction_status',
    )
    list_filter = (
        'transaction_type',
        'transaction_status',
        'date_created',
    )
    search_fields = (
        'mpesa_transaction_code',
        'receipt_ID',
        'user__username',
        'shop__branch_name',
        'customer_number',
    )
    readonly_fields = ('date_created',)

    # Inline to display associated products (ManyToManyField)
    filter_horizontal = ('products',)


admin.site.register(TransactionLog, TransactionLogAdmin)
