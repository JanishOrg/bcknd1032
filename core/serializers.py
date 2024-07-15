# core/serializers.py

from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import *
class CustomUsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUsers
        fields = '__all__'
class CustomUsersSerializers(serializers.ModelSerializer):
    class Meta:
        model = CustomUsers
        fields = ['username', 'full_name']
class CustomUserSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()
    class Meta:
        model = CustomUsers
        fields = [
            'id',
            'username',
            'full_name',            
            'email',
            'user_type',
            'password',
            'phone_number',
            'address',
            'gender',
            'adhaar_id',
            "driving_id",
            'profile_image',
            'updated',
            ]
        extra_kwargs = {
            'password': {'write_only': True},
        }
        # fields = '__all__'

    def create(self, validated_data):
        user = CustomUsers.objects.create_user(**validated_data)
        return user

class PDlction(serializers.ModelSerializer):


    
    class Meta:
        model = PDLocation
        fields = '__all__'
        
class PDLocationSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username')
    full_name = serializers.CharField(source='user.full_name')
    phone_number = serializers.CharField(source='user.phone_number')

    class Meta:
        model = PDLocation
        fields = ['current_latitude','current_longitude','destination_latitude', 'destination_longitude', 'pickup_address','destination_address', 'people_count', 'pickup_time', 'status', 'user_id', 'username', 'full_name','phone_number']
class PDLocationSerializer2(serializers.ModelSerializer):
    class Meta:
        model = PDLocation
        fields = '__all__'
class CustomUsersSerial(serializers.ModelSerializer):
    location = PDLocationSerializer()  # Assuming CustomUsers has a ForeignKey to PDLocation

    class Meta:
        model = CustomUsers
        # fields = ['current_latitude','current_longitude','destination_latitude', 'destination_longitude', 'destination_address', 'people_count', 'pickup_time', 'status', 'user_id', 'username', 'full_name']
        fields = ['location']
    

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        username = data.get('username')
        password = data.get('password')
        user = authenticate(username=username, password=password)
        if not user or not user.is_active:
            raise serializers.ValidationError("Incorrect username or password. Please try again.")

        data['user'] = user
        return data


class ForgotPasswordSerializer(serializers.Serializer):
    # phone_number = serializers.CharField(max_length=15)
    email = serializers.EmailField()

class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        # model = Location
        fields = '__all__'
        # fields = ['id', 'name', 'latitude', 'longitude']
class Dummyserial(serializers.Serializer):
   username = serializers.CharField(max_length=50)

class CustomSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUsers
        fields = ['id','is_accepted']

class PasswordUpdateSerializer(serializers.Serializer):
    otp = serializers.CharField(max_length=6, min_length=6)
    new_password = serializers.CharField(write_only=True)
class ChangePasswordSerializer(serializers.Serializer):
    user_id = serializers.CharField()
    password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True)



