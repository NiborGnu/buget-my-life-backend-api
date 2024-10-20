from rest_framework import serializers
from .models import Transaction, TransactionComment
from categories.models import Category


class TransactionSerializer(serializers.ModelSerializer):
    """Serializer for creating and updating Transaction instances."""
    category = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all()
    )

    class Meta:
        model = Transaction
        fields = [
            'id',
            'user',
            'amount',
            'transaction_type',
            'category',
            'description',
            'created_at',
            'updated_at',
            'recurring',
            'recurrence_interval',
            'recurrence_end_date'
        ]
        read_only_fields = ['user', 'created_at', 'updated_at']

    def create(self, validated_data):
        user = self.context['request'].user
        return Transaction.objects.create(user=user, **validated_data)

    def validate(self, data):
        # Ensure the selected category matches the transaction type
        if data['category'].category_type != data['transaction_type']:
            raise serializers.ValidationError(
                "Selected category does not match the transaction type."
            )
        return data

    def validate_amount(self, value):
        if value <= 0:
            raise serializers.ValidationError("Amount must be greater than zero.")
        return value


class TransactionCommentSerializer(serializers.ModelSerializer):
    """Serializer for creating and viewing comments on transactions."""
    
    class Meta:
        model = TransactionComment
        fields = ['id', 'transaction', 'user', 'comment']
        read_only_fields = ['user']

    def create(self, validated_data):
        # Automatically assign the user making the request to the comment
        user = self.context['request'].user
        return TransactionComment.objects.create(user=user, **validated_data)