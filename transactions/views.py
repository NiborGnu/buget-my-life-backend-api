from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from .models import Transaction, TransactionComment
from .serializers import TransactionSerializer, TransactionCommentSerializer

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

class TransactionCommentViewSet(viewsets.ModelViewSet):
    """ViewSet for managing TransactionComment instances."""
    permission_classes = [IsAuthenticated]
    queryset = TransactionComment.objects.all()
    serializer_class = TransactionCommentSerializer

    def get_queryset(self):
        return TransactionComment.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
