from rest_framework import serializers
from .models import *
from django.contrib.auth import get_user_model
User = get_user_model()


class UserRegistrationSerializer(serializers.ModelSerializer):
    mobile = serializers.CharField(max_length=10, min_length=10, help_text="Please enter mobile number")
    class Meta:
        model = User
        fields = ['mobile',]
    
    def validate(self, args):
        mobile = args.get('mobile', None)
        if mobile.isdigit() == False:
            raise serializers.ValidationError({'error' : ('Please enter the correct format of phone number.')})
        return super().validate(args)


class UserOTPVerifiySerializer(serializers.ModelSerializer):
    mobile = serializers.CharField(max_length=10, min_length=10, help_text="Please enter mobile number")
    otp = serializers.CharField(max_length=6, min_length=6, help_text="Please enter otp number")
    class Meta:
        model = User
        fields = ['mobile','otp',]

    def validate(self, args):
        otp = args.get('otp', None)
        mobile = args.get('mobile', None)
        if mobile.isdigit() == False:
            raise serializers.ValidationError({'error' : ('Please enter the correct format of phone number.')})
        return super().validate(args)
        if otp.isdigit() == False:
            raise serializers.ValidationError({'error' : ('Please enter the correct format of OTP number.')})
        return super().validate(args)


class MedicineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Medicine
        fields = '__all__'


## Upload User Prescription
class UserPrescriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserPrescription
        fields = ['image', ]


## Order History Serializer.
class OrderHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = UserOrderHistory
        fields = '__all__'


## User Shiping charge amount check.
class UserShippingChargeCheckSerializer(serializers.Serializer):
    amount = serializers.IntegerField()