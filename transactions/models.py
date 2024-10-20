from django.db import models
from users.models import User
from categories.models import Category
from django.utils import timezone

class Transaction(models.Model):
    """Model representing a financial transaction."""
    TRANSACTION_TYPES = (
        ('income', 'Income'),
        ('expense', 'Expense'),
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
    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        related_name='transactions'
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
    recurring = models.BooleanField(
        default=False
    )
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


class TransactionComment(models.Model):
    """Model for user-specific comments on a transaction."""
    transaction = models.ForeignKey(Transaction, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.user.username} on {self.transaction}"