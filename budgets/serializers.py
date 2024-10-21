from rest_framework import serializers
from .models import Budget
from categories.models import Category

class BudgetSerializer(serializers.ModelSerializer):
    """Serializer for the Budget model."""
    category = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.filter(
            category_type='expense'
        )
    )

    class Meta:
        model = Budget
        fields = [
            'id',
            'user',
            'category',
            'amount',
            'start_date',
            'end_date'
        ]
        read_only_fields = ['user']

    def validate(self, data):
        """Custom validation to ensure budget amount and date consistency."""
        if data['amount'] <= 0:
            raise serializers.ValidationError(
                "Budget amount must be greater than zero."
            )
        
        if data['end_date'] <= data['start_date']:
            raise serializers.ValidationError(
                "End date must be after the start date."
            )

        return data

    def create(self, validated_data):
        """Set the user and create a new budget."""
        user = self.context['request'].user
        return Budget.objects.create(user=user, **validated_data)
