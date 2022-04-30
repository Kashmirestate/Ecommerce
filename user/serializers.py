from rest_framework import serializers
from .models import *
class RegisterSerial(serializers.Serializer):
    email=serializers.CharField(allow_blank=False , required=True)
    address=serializers.CharField(allow_blank=False , required=True)
    password=serializers.CharField(allow_blank=False , required=True)
    type=serializers.CharField(allow_blank=False , required=True)
class getcatagoryserial(serializers.ModelSerializer):
    class Meta():
        model=catagory
        fields='__all__'

class getsubcatagoryserial(serializers.ModelSerializer):
    class Meta():
        model=SubCatagory
        fields='__all__'

