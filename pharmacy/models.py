from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from pharmacy.managers import CustomUserManager


## User Model class.
class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=100,unique=True,null=True, blank=True)
    first_name = models.CharField(max_length=100, null=True, blank=True)
    last_name = models.CharField(max_length=100, null=True, blank=True)
    username = models.CharField(max_length=100, null=True)
    mobile = models.CharField(max_length=14, unique=True)
    otp = models.CharField(max_length=6, null=True, blank=True)
    dob = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_on = models.DateTimeField(auto_now_add=True)
    USERNAME_FIELD = 'mobile'
    REQUIRED_FIELDS = ['username']
    objects = CustomUserManager()

    class Meta:
        db_table = 'users'
        indexes = [
            models.Index(fields=['mobile',]),
        ]


class Medicine(models.Model):
    name = models.CharField(max_length=300, unique=True)
    description = models.CharField(max_length=500, null=True, blank=True)
    image = models.ImageField(upload_to="medicine/image/", blank=True, null=True)
    price = models.FloatField()
    is_active = models.BooleanField(default=True)
    updated_on = models.DateTimeField(auto_now=True)
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'medicines'
        indexes = [
            models.Index(fields=['name',]),
        ]


class UserPrescription(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.FileField(upload_to="prescription/image/")
    updated_on = models.DateTimeField(auto_now=True)
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'user_prescriptions'
        indexes = [
            models.Index(fields=['user',]),
        ]


## Order History.
class UserOrderHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    medicine = models.ForeignKey(Medicine, on_delete=models.CASCADE)
    status = models.CharField(max_length=30)
    qty = models.IntegerField()
    price =  models.FloatField()
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'order_history'
        indexes = [
            models.Index(fields=['user','medicine', ]),
        ]
        

