from django.db import models

class Category(models.Model):
    """Model representing a category for a transaction."""
    CATEGORY_TYPES = (
        ('income', 'Income'),
        ('expense', 'Expense'),
    )

    name = models.CharField(max_length=55, unique=True)
    category_type = models.CharField(max_length=55, choices=CATEGORY_TYPES)
    parent_category = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name='subcategories'
    )

    class Meta:
        # Ensure the same name is not used for different types
        unique_together = ('name', 'category_type')

    def __str__(self):
        return f"{self.name} ({self.category_type})"
