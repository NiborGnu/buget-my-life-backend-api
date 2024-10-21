from django.db import models
from django.conf import settings
from categories.models import Category

class Budget(models.Model):
    """Model representing a budget for a category."""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE
    )
    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )
    start_date = models.DateField()
    end_date = models.DateField()

    class Meta:
        unique_together = (
            'user',
            'category',
            'start_date',
            'end_date'
        )

    def __str__(self):
        return f"{self.category} Budget for {self.user} from {self.start_date} to {self.end_date}"
