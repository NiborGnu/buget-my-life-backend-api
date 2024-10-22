from rest_framework import serializers
from .models import Goal

class GoalSerializer(serializers.ModelSerializer):
    progress = serializers.SerializerMethodField()
    completed = serializers.SerializerMethodField()

    class Meta:
        model = Goal
        fields = [
            'id',
            'title',
            'goal_type',
            'target_amount',
            'current_amount',
            'deadline',
            'progress',
            'completed',
            'created_at',
            'updated_at'
        ]

    def get_progress(self, obj):
        return obj.get_progress()

    def get_completed(self, obj):
        return obj.is_completed()

    def create(self, validated_data):
        user = self.context['request'].user
        return Goal.objects.create(user=user, **validated_data)