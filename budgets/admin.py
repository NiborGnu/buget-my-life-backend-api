from django.contrib import admin
from .models import Budget

class BudgetAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'category',
        'amount',
        'start_date',
        'end_date'
    )
    search_fields = (
        'user__username',
        'category__name'
    )

admin.site.register(Budget, BudgetAdmin)
