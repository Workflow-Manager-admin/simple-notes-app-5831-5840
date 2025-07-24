from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Note
from django.contrib.auth.password_validation import validate_password

# PUBLIC_INTERFACE
class NoteSerializer(serializers.ModelSerializer):
    """
    Serializer for Note model.
    """
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Note
        fields = ['id', 'title', 'content', 'created_at', 'updated_at', 'user']


# PUBLIC_INTERFACE
class UserRegistrationSerializer(serializers.ModelSerializer):
    """
    Serializer for registering a new user.
    """
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ['username', 'password', 'password2', 'email', 'first_name', 'last_name']

    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError({"password": "Passwords do not match."})
        return data

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

# PUBLIC_INTERFACE
class LoginSerializer(serializers.Serializer):
    """
    Serializer for user login.
    """
    username = serializers.CharField()
    password = serializers.CharField()
