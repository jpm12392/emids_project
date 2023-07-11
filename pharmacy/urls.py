from django.urls import path, include
from .views import *
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'medicine/pharmacy', MedicineView, 'medicine')
router.register(r'order/history', UserOrderHistory, 'history')

urlpatterns = [
    path('sign-up/', UserRegistrationAPIView.as_view(),name='signup'),
    path('verify-otp/', UserOTPValidateAPIView.as_view(),name='verify-otp'),
    path('', include(router.urls)),
    path('upload-prescription/', UploadUserPrescription.as_view(),name='upload-prescription'),
    path('shipping-charge/', UserShippingChargeCheck.as_view(),name='shipping-charge'),
   
    
]