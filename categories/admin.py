from django.contrib import admin
from .models import Category

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'category_type', 'parent_category')
    search_fields = ('name',)

admin.site.register(Category, CategoryAdmin)
