from django.db import models
from django.utils import timezone
from users.models import User

class Goal(models.Model):
    GOAL_TYPE_CHOICES = (
        ('saving', 'Saving'),
        ('debt', 'Debt'),
    )

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='goals'
    )
    title = models.CharField(max_length=155)
    goal_type = models.CharField(
        max_length=10,
        choices=GOAL_TYPE_CHOICES,
        default='saving'
    )
    target_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2)
    current_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0.00)
    deadline = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(
        default=timezone.now)
    updated_at = models.DateTimeField(
        auto_now=True)

    def __str__(self):
        return f"{self.title} - {self.get_goal_type_display()} Goal"

    def get_progress(self):
        if self.target_amount > 0:
            return (self.current_amount / self.target_amount) * 100
        return 0

    def is_completed(self):
        return self.current_amount >= self.target_amount
