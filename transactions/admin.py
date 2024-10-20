from django.contrib import admin
from .models import Transaction, TransactionComment

class TransactionAdmin(admin.ModelAdmin):
    list_display = ('user', 'amount', 'transaction_type', 'category', 'created_at')
    search_fields = ('user__username', 'amount', 'transaction_type', 'category__name')
    list_filter = ('transaction_type', 'category')

class TransactionCommentAdmin(admin.ModelAdmin):
    list_display = ('transaction', 'user', 'comment', 'created_at')
    search_fields = ('transaction__description', 'user__username', 'comment')

admin.site.register(Transaction, TransactionAdmin)
admin.site.register(TransactionComment, TransactionCommentAdmin)
