from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from .models import Transaction
from .serializers import TransactionSerializer

class TransactionViewSet(viewsets.ModelViewSet):
    """ViewSet for managing Transaction instances."""
    permission_classes = [IsAuthenticated]
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['transaction_type', 'category', 'recurring']

    def get_queryset(self):
        """Retrieve transactions for the authenticated user."""
        return Transaction.objects.filter(
            user=self.request.user
        )
