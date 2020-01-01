# django/rest_framework imports.
# from rest_framework import filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework.authentication import TokenAuthentication
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate

# app level imports
from .models import (
    User,
    Address,
)

from .serializer import(
    UserRegSerializer,
    UserLoginRequestSerializer,
    AddressSerializer,
    ListOfAddressSerializer,
    UpdateAddressSerializer,
)

# project level imports
from libs.constants import (
        BAD_REQUEST,
        BAD_ACTION,
)
from libs.exceptions import(
    ParseException,
    ResourceConflictException,
)

class UserViewSet(GenericViewSet):
    """
    """
    queryset = User.objects.all()
    # filter_backends = (filters.OrderingFilter, filters.SearchFilter)
    # ordering_fields = ('id',)
    ordering = ('id',)
    lookup_field = 'email'
    http_method_names = ['get', 'post', 'put', 'delete']

    serializers_dict = {
        'register': UserRegSerializer,
        'login': UserLoginRequestSerializer,      
    }

    def get_serializer_class(self):
        """
        """
        try:
            return self.serializers_dict[self.action]
        except KeyError as key:
            raise ParseException(BAD_ACTION, errors=key)

    @action(methods=['post'], detail=False)
    def register(self, request):
        '''
        User Registration.
        '''
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid() is False:
            raise ParseException(BAD_REQUEST, serializer.errors)

        try: 
             user = serializer.create(serializer.validated_data)
        except Exception as e:
            return Response(({'error':str(e)}), status=status.HTTP_409_CONFLICT)
        if user:
            return Response(serializer.validated_data, status=status.HTTP_201_CREATED)
            
        return Response(serializer.validated_data, status=status.HTTP_200_OK)

    @action(methods=['post'], detail=False)
    def login(self, request):
        '''
        User Login.
        '''
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid() is False:
            raise ParseException(BAD_REQUEST, serializer.errors)

        user = authenticate(
            username = serializer.validated_data["username"],
            email=serializer.validated_data["email"],
            password=serializer.validated_data["password"])

        if not user:
            return Response({'error': 'Invalid Credentials'},
                            status=status.HTTP_404_NOT_FOUND)
        token = user.access_token
        return Response({'token': token},
                        status=status.HTTP_200_OK)

    @action(
         methods=['post'], detail=False,
         permission_classes=[IsAuthenticated, ]
     )
    def logout(self, request):

        request.user.auth_token.delete()
        return Response({},status=status.HTTP_200_OK)


class AddressViewSet(GenericViewSet):
    """
    """
    permission_classes = [IsAuthenticated, ]
    # authentication_classes = (TokenAuthentication,)
    model = Address

    # queryset = Address.objects.all()
    http_method_names = ['get', 'post', 'put', 'delete']

    def get_queryset(self, filterdata=None):
        self.queryset = self.model.objects.all()
        if filterdata:
            self.queryset = self.queryset.filter(**filterdata)
        return self.queryset

    serializers_dict = {
        'add_address': AddressSerializer,
        'list_address': ListOfAddressSerializer,
        'delete_address': ListOfAddressSerializer,
        'update_address': UpdateAddressSerializer,
    }

    def get_serializer_class(self):
        """
        """
        try:
            return self.serializers_dict[self.action]
        except KeyError as key:
            raise ParseException(BAD_ACTION, errors=key)

    @action(methods=['post'], detail=False, url_path='add-address')
    def add_address(self, request):
           
        data = request.data
        data["user"] = request.user.id
        serializer = self.get_serializer(data=data)
        if serializer.is_valid() is False:
            raise ParseException(BAD_REQUEST, serializer.errors)

        user = serializer.save()
        if user:
            return Response(serializer.data, status=status.HTTP_201_CREATED)     
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(methods=['get'], detail=False, url_path='list-address')
    def list_address(self, request):
        """
        display address.
        """
        try:
            data = self.get_serializer(self.get_queryset(
                filterdata={"user": request.user}), many=True).data

            page = self.paginate_queryset(data)
            if page is not None:
                return self.get_paginated_response(page)

        except Exception as e:
            return Response({'error':str(e)},
             status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(methods=['delete'], detail=False, url_path='delete-address')
    def delete_address(self, request):
        """
        Delete the perticular address.
        """
        try:
            data = self.get_queryset(filterdata={"user": request.user,"id": request.data["id"]})
            data.delete()
            return Response(({"detail": "deleted successfully."}),
                status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error":str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['put'], detail=False, url_path='update-address')
    def update_address(self, request):
        """
        Modify the address details.
        """
        try:

            self.objects = self.model.objects.get(user_id=request.user, id=request.data['id'])
            
            serializer = self.get_serializer(self.objects, data=request.data)
            print(serializer.is_valid())
            print(serializer.errors)
            if serializer.is_valid() is False:
                raise ParseException(BAD_REQUEST, serializer.errors)

            user = serializer.save()
            print(user)
            if user:
                return Response({'detail':'updated successfully'},status=status.HTTP_200_OK)

        except Exception as e:
            return Response(({'error':'Failed', 'result':None, 'message':str(e)}),
                status=status.HTTP_400_BAD_REQUEST)






        


    