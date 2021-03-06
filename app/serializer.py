from rest_framework import serializers
from .models import Item, SellerAccount, Category
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model

UserModel = get_user_model()


class CreateUserSerializer(serializers.ModelSerializer):

    password2 = serializers.CharField(style={"input_type": "password"}, write_only=True)

    
    class Meta:
        model = UserModel
        fields = ( "email", "username", "password", "password2")
        extra_kwargs = {
            'password': {"write_only":True}
        }

    def save(self):
        password = self.validated_data['password']
        password2 = self.validated_data['password2']
        if password != password2:
            raise serializers.ValidationError({'password': 'Password must match'})
        user = UserModel.objects.create(
            email = self.validated_data['email'],
            username=self.validated_data['username']
        )
        user.set_password(self.validated_data['password'])
        user.save()

        return user





class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = (
            'name',
            'img',
        )

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (  
                    'first_name',
                    'last_name',
                    'email'
                )


class SellerSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = SellerAccount
        fields = ['user','is_aproved']


class ItemSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    class Meta:
        model = Item
        fields = (
                    'id',
                    'name',
                    'price',
                    'minimum_order',
                    'img',
                    'description',
                    'category',
                    'top_product',
                    'status'
                )
        read_only_fields = ('id', 'category','top_product',)


