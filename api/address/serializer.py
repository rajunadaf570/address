# django imports
from rest_framework import serializers

# app level imports
from .models import (
    User,
    Address,
)

class UserRegSerializer(serializers.ModelSerializer):
    """
    UserRegSerializer
    """
    username = serializers.CharField(required=True, min_length=2)
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True, min_length=5)
    first_name = serializers.CharField(required=True, min_length=2)
    last_name = serializers.CharField(required=True, min_length=2)

    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'email', 
            'password',           
            'first_name', 
            'last_name',               
        )
        write_only_fields = ('password',)
        read_only_fields = ('id',)

    def create(self, validated_data):
        user = User.objects.create(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user

class UserLoginRequestSerializer(serializers.Serializer):
    """
    UserLoginRequestSerializer.
    """
    username = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True, min_length=5)

    class Meta:
        model = User
        fields = (
            'first_name', 'last_name','access_token',
            'is_verified', 'password', 'email', 'username',
        )

class AddressSerializer(serializers.ModelSerializer):
    """
    """
    name = serializers.CharField(required=True, min_length=2)
    address1 = serializers.CharField(required=True, min_length=5)
    address2 = serializers.CharField(required=True, min_length=5)
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = Address
        fields = ('id', 'name', 'address1', 'address2', 'user', )

    def create(self, validated_data):
        user = Address.objects.create(**validated_data)
        user.save()
        return user

class ListOfAddressSerializer(serializers.ModelSerializer):
    """
    """
    class Meta:
        model = Address
        fields = (
            'id',
            'name',
            'address1',
            'address2',
        )

class UpdateAddressSerializer(serializers.ModelSerializer):
    """
    UpdateAddressSerializer
    """
    name = serializers.CharField(required=False)
    address1 = serializers.CharField(required=False)
    address2 = serializers.CharField(required=False)

    class Meta:
        model = Address
        fields = (
            'id',
            'name',
            'address1',
            'address2',
        )

    def validate(self, data):
        return data

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name')
        instance.address1 = validated_data.get('address1')
        instance.address2 = validated_data.get('address2')

        instance.save()
        return instance

