from transactions.models import Transaction
from .models import Goal

def update_goal_progress(user):
    # Update saving goals based on income
    saving_goals = Goal.objects.filter(user=user, goal_type='saving')
    for goal in saving_goals:
        transactions = Transaction.objects.filter(
            user=user,
            transaction_type='income'
        )
        total_saved = sum(
            transaction.amount for transaction in transactions
        )
        goal.current_amount = total_saved
        goal.save()

    # Update debt goals based on expense
    debt_goals = Goal.objects.filter(user=user, goal_type='debt')
    for goal in debt_goals:
        transactions = Transaction.objects.filter(
            user=user,
            transaction_type='expense'
        )
        total_paid = sum(
            transaction.amount for transaction in transactions
        )
        goal.current_amount = total_paid
        goal.save()