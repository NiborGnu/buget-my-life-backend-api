
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Goal
from .serializers import GoalSerializer

class GoalViewSet(viewsets.ModelViewSet):
    serializer_class = GoalSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Return only the goals belonging to the authenticated user
        return Goal.objects.filter(user=self.request.user)