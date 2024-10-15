from rest_framework import serializers
from dj_rest_auth.registration.serializers import RegisterSerializer
from rest_framework.validators import UniqueValidator
from allauth.account.adapter import get_adapter
from allauth.account.utils import setup_user_email
from users.models import User

class CustomRegisterSerializer(RegisterSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    username = serializers.CharField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )

    def get_cleaned_data(self):
        data = super().get_cleaned_data()
        data['email'] = self.validated_data.get('email', '')
        data['username'] = self.validated_data.get('username', '')
        return data

    def save(self, request):
        adapter = get_adapter()
        user = adapter.new_user(request)
        self.cleaned_data = self.get_cleaned_data()
        
        user.email = self.cleaned_data.get('email')
        user.username = self.cleaned_data.get('username')
        user.save()
        setup_user_email(request, user, [])

        adapter.save_user(request, user, self)
        return user
