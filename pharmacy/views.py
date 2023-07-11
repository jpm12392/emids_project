from django.shortcuts import render
from rest_framework.response import Response
from emids.jwt_tokens import generate_access_token, generate_refresh_token
from rest_framework import filters
from emids.paginations import MVPPagination
from rest_framework import viewsets
from rest_framework import generics, status, permissions
from rest_framework.parsers import FormParser, MultiPartParser
from .serializers import *


## User Registration.
class UserRegistrationAPIView(generics.GenericAPIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = UserRegistrationSerializer

    def post(self, request):
        try:
            serializer = self.serializer_class(data=request.data)
            if serializer.is_valid():
                import random
                otp = random.randrange(111111, 999999, 6)
                if User.objects.filter(mobile=request.data['mobile']).exists():
                    User.objects.filter(mobile=request.data['mobile']).update(otp=otp)
                else:
                    User.objects.create(mobile=request.data['mobile'],username=request.data['mobile'],otp=otp)
                context = {'status': True,'message': 'User has been added successfully.','data': [{'otp':otp,'mobile':request.data['mobile']}]}
                return Response(context, status=status.HTTP_200_OK)
            
            context = {'status': False,'message': serializer.errors}
            return Response(context, status=status.HTTP_200_OK)
        except Exception as e:
            context = {'status': False, 'message': 'Something Went Wrong'}
            return Response(context, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


## User OTP Validate.
class UserOTPValidateAPIView(generics.GenericAPIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = UserOTPVerifiySerializer

    def post(self, request, *args, **kwargs):
        try:
            serializer = self.serializer_class(data=request.data)
            if serializer.is_valid():
                if User.objects.filter(otp=request.data['otp'], mobile=request.data['mobile']).exists():
                    user = User.objects.filter(mobile=request.data['mobile']).first()
                    access_token = generate_access_token(user.id)
                    refresh_token = generate_refresh_token(user.id)
                    context = {'status': True, 'massage': 'Login Successfully',"access_token": access_token,"refresh_token": refresh_token,}
                else:
                    context = {'status': False,'message': 'OTP is wrong.',}
            else:
                context = {'status': False,'message': serializer.errors}
            return Response(context, status=status.HTTP_200_OK)
        except Exception as e:
            context = {'status': False, 'message': 'Something Went Wrong'}
            return Response(context, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


## Medicine Viewset.
class MedicineView(viewsets.ModelViewSet):
    permission_classes = (permissions.AllowAny,)
    serializer_class = MedicineSerializer
    queryset = Medicine.objects.all().order_by('-created_on')   ## Medicine Model
    pagination_class = MVPPagination
    filter_backends = [filters.SearchFilter]
    search_fields = ['name',]


# Upload UserPrescription.
class UploadUserPrescription(generics.GenericAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = UserPrescriptionSerializer
    parser_classes = (FormParser, MultiPartParser)

    def post(self, request, *args, **kwargs):
        try:
            serializer = self.serializer_class(data=request.data)
            if serializer.is_valid():
                serializer.save(user=self.request.user)
                context = {'status': True, 'massage': 'Uploaded Successfully'}
            else:
                context = {'status': False,'message': serializer.errors}
            return Response(context, status=status.HTTP_200_OK)
        except Exception as e:
            context = {'status': False, 'message': 'Something Went Wrong'}
            return Response(context, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


## User Order History VIewset.
class UserOrderHistory(viewsets.ModelViewSet):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = OrderHistorySerializer
    queryset = UserOrderHistory.objects.select_related('user','medicine').all().order_by('-created_on')   ## Order History Model
    pagination_class = MVPPagination
    filter_backends = [filters.SearchFilter]
    search_fields = ['qty',]


## Check User Shipping Charges.
class UserShippingChargeCheck(generics.GenericAPIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = UserShippingChargeCheckSerializer

    def post(self, request, *args, **kwargs):
        try:
            serializer = self.serializer_class(data=request.data)
            if serializer.is_valid():
                if request.data.get('amount') < 1000:
                    context = {'status': True, 'massage': 'Shipping charges apply'}
                else:
                    context = {'status': True, 'massage': 'No Shipping charges apply'}
                
            else:
                context = {'status': False,'message': serializer.errors}
            return Response(context, status=status.HTTP_200_OK)
        except Exception as e:
            context = {'status': False, 'message': 'Something Went Wrong'}
            return Response(context, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

