from django.db import models
from users.models import User
from django.utils import timezone

class Transaction(models.Model):
    """Model representing a financial transaction."""
    TRANSACTION_TYPES = (
        ('income', 'Income'),
        ('expense', 'Expense'),
        ('transfer', 'Transfer'),  # Future feature
    )

    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='transactions'
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_type = models.CharField(
        max_length=10, 
        choices=TRANSACTION_TYPES
    )
    category = models.CharField(
        max_length=100, 
        null=True, 
        blank=True
    )
    description = models.TextField(
        null=True, 
        blank=True
    )
    created_at = models.DateTimeField(
        default=timezone.now
    )
    updated_at = models.DateTimeField(
        auto_now=True
    )
    recurring = models.BooleanField(default=False)
    recurrence_interval = models.CharField(
        max_length=10, 
        null=True, 
        blank=True
    )
    recurrence_end_date = models.DateField(
        null=True, 
        blank=True
    )
    last_occurrence_date = models.DateTimeField(
        null=True,
        blank=True
    )

    def __str__(self):
        """Return a string representation of the transaction."""
        return f"{self.transaction_type.capitalize()} - ${self.amount:.2f} on {self.created_at}"
