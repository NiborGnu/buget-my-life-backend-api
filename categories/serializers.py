from rest_framework import serializers
from .models import Category
from transactions.models import Transaction  # Import Transaction model

class CategorySerializer(serializers.ModelSerializer):
    """Serializer for the Category model."""
    
    class Meta:
        model = Category
        fields = ['id', 'name', 'category_type', 'parent_category']

class TransactionSerializer(serializers.ModelSerializer):
    """Serializer for creating and updating Transaction instances."""
    category = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(),
        required=True
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
        """Create a new Transaction instance."""
        user = self.context['request'].user  # Get the user from the request context
        return Transaction.objects.create(user=user, **validated_data)

    def validate(self, data):
        """Perform custom validation for Transaction data."""
        # Ensure that the amount is positive
        if data.get('amount', 0) <= 0:
            raise serializers.ValidationError(
                "Amount must be greater than zero."
            )

        # Ensure recurrence interval is provided for recurring transactions
        if data.get('recurring') and not data.get('recurrence_interval'):
            raise serializers.ValidationError(
                "Recurrence interval is required for recurring transactions."
            )

        # Ensure the selected category matches the transaction type
        if data['category'].category_type != data['transaction_type']:
            raise serializers.ValidationError(
                "Selected category does not match the transaction type."
            )

        return data

    def update(self, instance, validated_data):
        """Update an existing Transaction instance."""
        for field in validated_data:
            setattr(instance, field, validated_data[field])

        # Save the updated instance
        instance.save()
        return instance
