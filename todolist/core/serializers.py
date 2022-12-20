# from core.models import User
# from rest_framework.exceptions import ValidationError, AuthenticationFailed, NotAuthenticated

from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.hashers import make_password
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.exceptions import ValidationError, AuthenticationFailed, NotAuthenticated


USER_MODEL = get_user_model()


class RegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    password_repeat = serializers.CharField(write_only=True)

    def validate(self, attrs):
        # if attrs['password'] != attrs['password_repeat']:
        #     raise ValidationError("password and password_repeat is not equal")
        # return attrs
        password = attrs.get('attrs')
        password_repeat = attrs.pop('password_repeat')

        try:
            validate_password(password)
        except Exception as e:
            raise serializers.ValidationError({'password': e.args[0]})

        if password != password_repeat:
            raise serializers.ValidationError("Passwords don't match")
        return attrs

    def create(self, validated_data):
        password = validated_data.get('password')
        validated_data['password'] = make_password(password)
        instance = super().create(validated_data)
        return instance

    class Meta:
        model = USER_MODEL
        fields = '__all__'


class LoginSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True)

    def create(self, validated_data):
        if not (user := authenticate(
                username=validated_data['username'],
                password=validated_data['password']
        )):
            raise AuthenticationFailed
        return user

    class Meta:
        model = USER_MODEL
        fields = '__all__'


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = USER_MODEL
        fields = (
            "id",
            "username",
            "first_name",
            "last_name",
            "email",
        )


class UpdatePasswordSerializer(serializers.Serializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    old_password = serializers.CharField(required=True, write_only=True)
    new_password = serializers.CharField(required=True, write_only=True)

    def validate(self, attrs):
        if not (user := attrs['user']):
            raise NotAuthenticated
        if not user.check_password(attrs['old_password']):
            raise serializers.ValidationError({'old_password': 'incorrect password'})
        return attrs

    def create(self, validated_data: dict):
        raise NotImplementedError

    def update(self, instance: user, validated_data):
        instance.password = make_password(validated_data['new_password'])
        instance.save(update_fields=('password',))
        return instance


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = USER_MODEL
        fields = ('id', 'username', 'first_name', 'last_name', 'email')
