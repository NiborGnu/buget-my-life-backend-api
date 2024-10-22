from rest_framework import views
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Sum
from transactions.models import Transaction
from .serializers import ReportFilterSerializer

class ReportView(views.APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = ReportFilterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Extract validated data
        start_date = serializer.validated_data['start_date']
        end_date = serializer.validated_data['end_date']
        category = serializer.validated_data.get('category')
        report_type = serializer.validated_data['report_type']

        # Query transactions based on filters
        transactions = Transaction.objects.filter(
            user=request.user,
            created_at__range=[start_date, end_date]
        )

        if category:
            transactions = transactions.filter(category=category)

        if report_type != 'all':
            transactions = transactions.filter(transaction_type=report_type)

        # Aggregate totals by category
        report_data = transactions.values(
            'category__name'
        ).annotate(total_amount=Sum('amount')).order_by('-total_amount')

        return Response(report_data)
