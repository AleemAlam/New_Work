from rest_framework.views import APIView
from rest_framework.response import Response
from .serializer import ItemSerializer, UserSerializer, CreateUserSerializer
from rest_framework.exceptions import ValidationError
from rest_framework.decorators import api_view
from rest_framework import generics
from .models import Item, SellerAccount, Category
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status
from rest_framework.permissions import IsAdminUser
from rest_framework.decorators import api_view


# ITEM

class ItemView(APIView):
    def get(self, request):
        if request.user.is_authenticated and request.user.is_staff:
            items = Item.objects.filter(seller__user = request.user)
            serializer = ItemSerializer(items, many=True)
            return Response(serializer.data)
        else:
            return Response({'Invalid User'})

    
    def post(self, request, format=None):
        if request.user.is_authenticated and request.user.is_staff:
            data = request.data
            seller = SellerAccount.objects.get(user = request.user)
            try:
                category = Category.objects.get(name = data['category'])
            except ObjectDoesNotExist:
                raise ValidationError('Invalid Category')
            item = Item.objects.create(
                seller = seller,
                name = data['name'], 
                price = data['price'],
                minimum_order = data['minimum_order'],
                description = data['description'],
                top_product = False,
                category = category,
                status = 'offline',
            )
            return Response({'message':'Item Aded'})
        else:
            return Response({'Invalid User'})

class ItemCrudView(APIView):
    def get_object(self, pk):
        try:
            return Item.objects.get(pk=pk , seller__user = self.request.user)
        except Item.DoesNotExist:
            raise ValidationError('Product id is invalid')
        except:
            raise ValidationError('Invalid User')


    def get(self, request,pk):
        if request.user.is_authenticated and request.user.is_staff:
            item = self.get_object(pk)
            serializer = ItemSerializer(item, many=False)
            return Response(serializer.data)
        else:
            return Response({'message': 'Please Login'})

    def put(self, request, pk, format=None):
        if request.user.is_authenticated and request.user.is_staff:
            item = self.get_object(pk)
            serializer = ItemSerializer(item, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            raise ValidationError('You need to Login First')
            
    
    def delete(self, request, pk):
        if request.user.is_authenticated and request.user.is_staff:
            item = self.get_object(pk)
            item.delete()
            return Response({'message':'Item Deleted'})
        else:
            return Response({'message':'Please Login'})


#SELLER


class SellerCreateView(APIView):
    def post(self, request):
        serializer = CreateUserSerializer(data = request.data)
        data = {}
        if serializer.is_valid():
            new_user = serializer.save()
            new_user.is_staff = True
            new_user.save()
            new_seller = SellerAccount.objects.create(user = new_user)
            data['response'] = "User Created Successfully"
            data['username'] = new_user.username
            data['email'] = new_user.email
        else:
            data = serializer.errors
        return Response(data)       

class SellerCrudView(APIView):
    def res_content(self, u):
        try:    
            seller = SellerAccount.objects.get(user = u)
        except :
            raise ValidationError('Invalid User')
        return {
                "user":{ 
                    "username": u.username,
                    "first_name": u.first_name,
                    "last_name": u.last_name,
                    "email": u.email,
                },
                "is_aproved": seller.is_aproved
        }


    def get(self, request, format=None, **kwargs):
        if request.user.is_authenticated and request.user.is_staff:
            content = self.res_content(request.user)
            return Response(content)
        else:
            return Response({'message':'Please Login'})

    def put(self, request, format=None, **kwargs):
        if request.user.is_authenticated and request.user.is_staff:
            user = User.objects.get(id = request.user.id )
            serializer = UserSerializer(user, data = request.data)
            if serializer.is_valid():
                updated_user = serializer.save()
                content = {
                    "first_name": updated_user.first_name,
                    "last_name": updated_user.last_name,
                    "email": updated_user.email
                }
                return Response(content)
            return Response(serializer.data)
        else:
            return Response({'message':'Please Login'})

    def delete(self, request):
        if request.user.is_authenticated and request.user.is_staff:
            user = User.objects.get(username = request.user.username)
            user.delete()
            return Response({'message':'user Deleted'})
        else:
            return Response({'message':'Please Login'})


    

    

                
