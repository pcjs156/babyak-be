from rest_framework import serializers

from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'name']


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    password = serializers.CharField(max_length=128, write_only=True)

    def validate(self, data):
        username = data.get('username')
        password = data.get('password')

        if not (username and password):
            raise serializers.ValidationError('Required fields: username, password')

        return {
            'username': username,
            'password': password
        }


class RegistrationSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=150)
    password = serializers.CharField(
        max_length = 128,
        write_only = True
    )    
    name = serializers.CharField(max_length=100)
    class Meta:
        model = User
        fields = [
            'username',
            'password',
            'name'
            ]
        
    def create(self, validated_data):
        return User.objects.create_user(**validated_data)