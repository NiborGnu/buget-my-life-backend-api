from .models import Transaction
from datetime import timedelta, date
from django.utils import timezone

def handle_recurring_transactions():
    """Process recurring transactions and create new transactions 
    based on the recurrence rules."""
    today = timezone.now()
    recurring_transactions = Transaction.objects.filter(
        recurring=True,
        recurrence_end_date__gte=today
    )

    for transaction in recurring_transactions:
        next_occurrence = calculate_next_occurrence(transaction)
        
        if next_occurrence <= today:
            create_transaction(transaction)
            # Update the last_occurrence_date
            transaction.last_occurrence_date = today
            transaction.save()

def create_transaction(transaction):
    """Create a new transaction based on the recurring transaction 
    details."""
    Transaction.objects.create(
        user=transaction.user,
        amount=transaction.amount,
        transaction_type=transaction.transaction_type,
        category=transaction.category,
        description=(
            f"Recurring: {transaction.description}"
        ),
        recurring=False  # The new transaction isn't recurring
    )

def is_leap_year(year):
    """Check if the given year is a leap year."""
    return (
        (year % 4 == 0 and year % 100 != 0) 
        or (year % 400 == 0)
    )

def calculate_next_occurrence(transaction):
    """Calculate the next occurrence date based on transaction 
    recurrence."""
    last_occurrence = transaction.last_occurrence_date or transaction.created_at

    if transaction.recurrence_interval == 'daily':
        return last_occurrence + timedelta(days=1)

    if transaction.recurrence_interval == 'weekly':
        return last_occurrence + timedelta(weeks=1)

    if transaction.recurrence_interval == 'monthly':
        next_month = last_occurrence.month + 1
        next_year = last_occurrence.year
        
        if next_month > 12:
            next_month = 1
            next_year += 1

        try:
            return last_occurrence.replace(
                month=next_month, 
                year=next_year
            )
        except ValueError:
            return handle_invalid_day(
                next_month,
                next_year,
                last_occurrence.day,
                last_occurrence
            )

    return last_occurrence

def handle_invalid_day(
    next_month, 
    next_year, 
    day_of_month, 
    last_occurrence
):
    """Adjust the day for months with fewer days than the last 
    occurrence."""
    if next_month in [1, 3, 5, 7, 8, 10, 12]:  # Months with 31 days
        day = 31
    elif next_month == 2:  # February
        day = (
            29 if is_leap_year(next_year) 
            else 28  # Non-leap year, February has 28 days
        )
    else:  # Months with 30 days
        day = 30

    return last_occurrence.replace(
        month=next_month,
        year=next_year,
        day=day
    )
