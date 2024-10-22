from rest_framework import serializers
from categories.models import Category

class ReportFilterSerializer(serializers.Serializer):
    start_date = serializers.DateField()
    end_date = serializers.DateField()
    category = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(),
        required=False
    )
    report_type = serializers.ChoiceField(
        choices=[
            (
                'income',
                'Income'
            ),
            (
                'expense',
                'Expense'
            ),
            (
                'all',
                'All'
            )
        ],
        default='all'
    )
