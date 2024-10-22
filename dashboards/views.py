from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Sum
from datetime import date
from transactions.models import Transaction
from budgets.models import Budget
from goals.models import Goal

class DashboardView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user

        # Total income and expenses for the current month
        today = date.today()
        month_start = today.replace(day=1)
        income = Transaction.objects.filter(user=user, transaction_type='income', date__gte=month_start).aggregate(total_income=Sum('amount'))['total_income'] or 0
        expenses = Transaction.objects.filter(user=user, transaction_type='expense', date__gte=month_start).aggregate(total_expenses=Sum('amount'))['total_expenses'] or 0

        # Budget utilization (sum of all budgets vs. total spent)
        budgets = Budget.objects.filter(user=user)
        total_budget = budgets.aggregate(total_budget=Sum('amount'))['total_budget'] or 0
        total_spent = Transaction.objects.filter(user=user, transaction_type='expense', date__gte=month_start).aggregate(total_spent=Sum('amount'))['total_spent'] or 0

        # Goal progress (for all active goals)
        goals = Goal.objects.filter(user=user)
        goal_data = [{
            'title': goal.title,
            'goal_type': goal.goal_type,
            'target_amount': goal.target_amount,
            'current_amount': goal.current_amount,
            'progress': goal.get_progress(),
            'completed': goal.is_completed(),
        } for goal in goals]

        # Recent transactions (limit to 5 latest transactions)
        recent_transactions = Transaction.objects.filter(user=user).order_by('-date')[:5]
        transaction_data = [{
            'id': transaction.id,
            'amount': transaction.amount,
            'category': transaction.category.name if transaction.category else None,
            'transaction_type': transaction.transaction_type,
            'date': transaction.date.strftime('%Y-%m-%d')  # Formatting date
        } for transaction in recent_transactions]

        # Consolidating all the data into the dashboard response
        dashboard_data = {
            'total_income': income,
            'total_expenses': expenses,
            'total_budget': total_budget,
            'total_spent': total_spent,
            'budget_utilization': (total_spent / total_budget * 100) if total_budget > 0 else 0,
            'goals': goal_data,
            'recent_transactions': transaction_data,
        }

        return Response(dashboard_data)