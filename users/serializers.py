from django.contrib.auth import password_validation
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from users.models import Balance, User

class RegistrationUserSerializer(serializers.ModelSerializer):
    
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password2']
        extra_kwargs = {'password': {'write_only': True}}


    def validate_password(self, value):
        try:
            password_validation.validate_password(value)
        except ValidationError as exc:
            raise serializers.ValidationError(str(exc))
        return value
    
    def validate(self, attrs):
        attrs = super().validate(attrs)
        if attrs['password'] != attrs['password2']:
            raise ValidationError({"password": "Пароли не совпадают."})
        return attrs

    def create(self, validated_data):
        
        validated_data.pop('password2')
        
        user = User.objects.create_user(**validated_data)
        
        return user


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'post', 'balance']
        extra_kwargs = {'balance': {'read_only': True}}



class BalanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Balance
        fields = ['id', 'owner', 'amount']