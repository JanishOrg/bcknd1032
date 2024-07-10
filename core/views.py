from rest_framework import status
from django.http import JsonResponse
from geopy.geocoders import Nominatim
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import *
from .models import *
from decimal import Decimal
from rest_framework.permissions import AllowAny ,IsAuthenticated
from rest_framework.decorators import permission_classes
from django.contrib.auth import logout
from django.core.mail import send_mail
from django.utils.crypto import get_random_string
from rest_framework import serializers, status, views
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.response import Response
from geopy.distance import geodesic
from .serializers import CustomUserSerializer, LocationSerializer
from rest_framework.decorators import api_view
import json
# Added new files
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from django.core.mail import EmailMessage


# class NearbyDriversAPIView(generics.ListAPIView):
#     serializer_class = CustomUserSerializer
#     def get(self, request, user_id):
#         user = CustomUsers.objects.get(id=user_id)
#         user_latitude = user.user_location.latitude
#         user_longitude = user.user_location.longitude
#         nearby_locations = self.get_queryset(user_latitude, user_longitude)
#         updated_location_ids = []
#         for location in nearby_locations:
#             address = self.get_address_from_coordinates(location.latitude, location.longitude)
#             serializer = CustomUserSerializer(location.user)
#             serializer_data = serializer.data
#             serializer_data['loaction_address'] = address
#             updated_serializer = CustomUserSerializer(location.user, data=serializer_data, partial=True)
#             if updated_serializer.is_valid():
#                 updated_serializer.save(loaction_address=address)
#             updated_location_ids.append(str(location.id))
#         return Response({"message": str(updated_location_ids)})
    

#     def get_address_from_coordinates(self, latitude, longitude):
#         geolocator = Nominatim(user_agent="my_geocoder")

#         try:
#             location = geolocator.reverse((latitude, longitude), language='en', timeout=10)
#             return location.address if location else None
#         except Exception as e:
#             print(f"Error: {e}")
#             return None
        
                
#     def get_queryset(self, user_latitude, user_longitude):
#         drivers = CustomUsers.objects.filter(user_type='driver')
#         nearby_locations = []
#         for driver in drivers:
#             location_coords = (float(driver.user_location.latitude), float(driver.user_location.longitude))
#             user_coords = (user_latitude, user_longitude)
#             distance = geodesic(user_coords, location_coords).kilometers
#             if distance <= 1:
#                 nearby_locations.append(driver.user_location)
#         print(nearby_locations)
#         return nearby_locations
    
# class NearbyDriversAPIView(generics.ListAPIView):
#     serializer_class = CustomUserSerializer
#     def get(self, request, user_id):
#         user = CustomUsers.objects.get(id=user_id)
#         user_latitude = float(user.location.pickup_latitude)
#         user_longitude = float(user.location.pickup_longitude)
#         nearby_drivers = self.get_queryset(user_latitude, user_longitude)
#         updated_location_ids = []
#         for driver in nearby_drivers:
#             address = self.get_address_from_coordinates(float(driver.pickup_latitude), float(driver.pickup_longitude))
#             serializer = CustomUserSerializer(driver.user)
#             serializer_data = serializer.data
#             serializer_data['loaction_address'] = address
#             updated_serializer = CustomUserSerializer(driver.user, data=serializer_data, partial=True)
#             if updated_serializer.is_valid():
#                 if address == None:
#                     updated_location_ids.append(str(driver.id))
#                 else :
#                     updated_serializer.save(loaction_address=address)
#                     updated_location_ids.append(str(driver.id))

#         return Response({"message": str(updated_location_ids)})
#     def get_address_from_coordinates(self, latitude, longitude):
#         geolocator = Nominatim(user_agent="my_geocoder")

#         try:
#             location = geolocator.reverse((latitude, longitude), language='en', timeout=10)
#             print(location)
#             return location.address if location else None
#         except Exception as e:
#             print(f"Error: {e}")
#             return None
#     def get_queryset(self, user_latitude, user_longitude):
#         nearby_drivers = PDLocation.objects.filter(
#             pickup_latitude__range=(Decimal(str(user_latitude)) - Decimal('0.01'), Decimal(str(user_latitude)) + Decimal('0.01')),
#             pickup_longitude__range=(Decimal(str(user_longitude)) - Decimal('0.01'), Decimal(str(user_longitude)) + Decimal('0.01')),
#         )
#         print(nearby_drivers)
#         return nearby_drivers
    

class CustomUserAPIView(APIView):
    def get(self, request, pk=None):
        if pk is not None:
            try:
                user = CustomUsers.objects.get(pk=pk)
                serializer = CustomUserSerializer(user)
                return Response(serializer.data)
            except CustomUsers.DoesNotExist:
                return Response({"error": "Custom user not found"}, status=status.HTTP_404_NOT_FOUND)
        else:
            queryset = CustomUsers.objects.all()
            serializer = CustomUserSerializer(queryset, many=True)
            return Response(serializer.data)

    def is_duplicate_value(self, field_name, value):
        return CustomUsers.objects.filter(**{field_name: value}).exists()

    def post(self, request):
        username = request.data.get('username')
        phone_number = request.data.get('phone_number')
        email = request.data.get('email')
        if self.is_duplicate_value('username', username):
            print("Username already exists.")
            main= "Username already exists."    
            return Response({"asgi": main}, status=status.HTTP_400_BAD_REQUEST)
        elif self.is_duplicate_value('phone_number', phone_number):
            print("Phone number already exists.")
            return Response({"asgi": "Phone number already exists."}, status=status.HTTP_400_BAD_REQUEST)
        elif self.is_duplicate_value('email', email):
            print("Email already exists.")
            return Response({"asgi": "Email already exists."}, status=status.HTTP_400_BAD_REQUEST)

        serializer = CustomUserSerializer(data=request.data)        
        if serializer.is_valid():
            print(serializer)
            serializer.save()
            main = serializer.data
            return Response({"asgi": main}, status=status.HTTP_201_CREATED)
        errors = serializer.errors
        print(errors)
        return Response({'error': "Bad Request", 'errors': errors}, status=status.HTTP_400_BAD_REQUEST)
        # return Response({"error": "Email already exists."}, )

    def patch(self, request, pk):
        instance = CustomUsers.objects.get(pk=pk)
        serializer = CustomUserSerializer(instance, data=request.data, partial=True)
        print(serializer)
        if serializer.is_valid():
            serializer.save()
            return Response({'ok':"Your Profile Updated successfully"})
        else:
            errors = serializer.errors
            print(errors)
            return Response({'error': "Bad Request", 'errors': errors}, status=status.HTTP_400_BAD_REQUEST)
        
class LoginAPIView(APIView):
    serializer_class = LoginSerializer
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        print(serializer)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        response_data = {
            'user_id': user.id,
            'Profile_Updated': user.updated,
            'Login':'Successfully'
        }
        print(response_data)
        return Response({'main':response_data}, status=status.HTTP_200_OK)

class UserTypeListView(APIView):
    def get(self, request):
        user_type = self.kwargs.get('user_type')
        print(user_type)
        if not user_type:
            return Response({'error': 'User type parameter is required'}, status=status.HTTP_400_BAD_REQUEST)
        users = CustomUsers.objects.filter(user_type=user_type)
        data = [{'full_name': user.full_name, 'email': user.email, 'phone_number': user.phone_number} for user in users]
        return Response(data, status=status.HTTP_200_OK)


# @permission_classes([IsAuthenticated])
class LogoutAPIView(APIView):
    def post(self, request, *args, **kwargs):
        user_id = request.data.get('user_id')
        print(user_id)
        try:
            user = CustomUsers.objects.get(id=user_id)
        except CustomUsers.DoesNotExist:
            return Response({'detail': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)

        logout(request)
        return Response({'detail': 'Successfully logged out.'}, status=status.HTTP_200_OK)


class PasswordUpdateView(views.APIView):
    def post(self, request, *args, **kwargs):
        serializer = PasswordUpdateSerializer(data=request.data)
        print(request.data)
        user = request.data.get('user')
        if serializer.is_valid():
            otp = serializer.validated_data['otp']
            new_password = serializer.validated_data['new_password']
            
            # Validate OTP
            user = self.verify_otp(user, otp)
            print(user)
            if user:
                # Update the password
                user.set_password(new_password)
                user.save()

                # Delete the used OTP
                OTP.objects.filter(user=user, otp=otp).delete()

                return Response({'ok': 'Password updated successfully'})
            else:
                return Response({'error': 'Invalid OTP'}, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def verify_otp(self, user, otp):
        # Check if the OTP is valid for the given user
        try:
            otp_obj = OTP.objects.get(user=user, otp=otp)
            return otp_obj.user
        except OTP.DoesNotExist:
            return None
        
class ChangePasswordView(APIView):
    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data)        
        if serializer.is_valid():
            user_id = serializer.validated_data['user_id']
            new_password = serializer.validated_data['new_password']
            password = serializer.validated_data['password']            
            try:
                user = CustomUsers.objects.get(id=user_id)
            except CustomUsers.DoesNotExist:
                return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)            
            if not user.check_password(password):
                return Response({'message': 'Old password is incorrect'}, status=status.HTTP_400_BAD_REQUEST)            
            user.set_password(new_password)
            user.save()
            return Response({'message': 'Password changed successfully'}, status=status.HTTP_200_OK)        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class ForgotPasswordView(views.APIView):
    def post(self, request, *args, **kwargs):
        serializer = ForgotPasswordSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            user = CustomUsers.objects.get(email=email)
            print(user)
            otp_code = get_random_string(length=6, allowed_chars='1234567890')
            OTP.objects.create(user=user, otp=otp_code)
            subject = 'Password Reset OTP'
            message = f'Your OTP for password reset is: {otp_code}'
            sender = "noreply@ramo.co.in"
            print(message)
            from_email = 'sonalisharma7224@gmail.com'
            recipient_list = [email]

            # send_mail(subject, message, from_email, recipient_list)
            try:
                # Using Django's EmailMessage
                email = EmailMessage(subject, message, sender, recipient_list)
                email.send()
        
            except Exception as e:
                # Handle email sending failure
                return Response({'success': False, 'message': 'Error sending email', 'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            print("ok")
            return Response({'ok': 'OTP sent successfully'})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PDLocationCreateAPIView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = PDLocationSerializer(data=request.data)
        print(serializer)
        if serializer.is_valid():
            location_instance = serializer.save()
            user_instance = location_instance.user
            user_instance.location = location_instance
            user_instance.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class testoo(APIView):
    def get(self,request,id):
        deppkadalla = PDLocation.objects.get(id=id)
        print(deppkadalla.user)
        return Response({"main":"deppkadalla"}, status=status.HTTP_200_OK)
    
class Search(APIView):
    def get(self, request, username):
        try:
            user = CustomUsers.objects.get(username=username)
            serializer = CustomUsersSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except CustomUsers.DoesNotExist:
            return Response({"error": f"User with username '{username}' not found."}, status=status.HTTP_404_NOT_FOUND)
    

class PDLocationAPIView(APIView):
    def get(self, request, pk,format=None):
        user = CustomUsers.objects.get(id=pk)
        print("kerbgarbrgawkjebg",user)
        # users = CustomUsers.objects.filter(location__status=1,vehicle_type=user.vehicle_type)
        users = CustomUsers.objects.filter(location__status=1)
        serializer = CustomUsersSerial(users, many=True)
        return Response(serializer.data)

# class PDLocationAPIView(APIView):
#     def get(self, request, format=None):
#         # user = CustomUsers.objects.filter(location__status=1)
#         users = CustomUsers.objects.filter(location__status=1)
#         serializer = CustomUsersSerial(users, many=True)
#         return Response(serializer.data)

class PDLocationDetailAPIView(APIView):
    def patch(self, request, pk, format=None):
        try:
            user = CustomUsers.objects.get(pk=pk)
            pd_location = user.location
        except PDLocation.DoesNotExist:
            return Response({"error": "PDLocation not found"}, status=status.HTTP_404_NOT_FOUND)        
        serializer = PDLocationSerializer(pd_location, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
class dfd(APIView):
    def post(self,request,pk,fromat=None):
        print(pk)
        user_id = request.data.get('user_id')
        user = CustomUsers.objects.get(id=user_id)
        print(user.location.acpted_driver)  
        if user.location.acpted_driver == pk and user.location.status == 3:
            serializer = PDlction(user.location)
            return Response(serializer.data)    
        else:
            return Response("{}")    

class PDLocationAPIView2(APIView):

    def get(self, request, pk, format=None):
        try:
            drive = CustomUsers.objects.get(pk=pk)
            pd_location = drive.location
            print(drive)
        except PDLocation.DoesNotExist:
            return Response({"error": "PDLocation not found"}, status=status.HTTP_404_NOT_FOUND)        
        serializer = PDLocationSerializer2(pd_location)
        if pd_location.status == 2:
            print("rajus")
            driver = CustomUsers.objects.get(id=pd_location.acpted_driver)
            print(driver)
            dict = {
                "driver_id":pd_location.acpted_driver,
                "driver_contact":driver.email,
                "driver_full_name":driver.full_name,
                "driver_phone_number":driver.phone_number,
                # "driver_profile_image":driver.profile_image,
            }
            return Response(dict, status=status.HTTP_200_OK)
        return Response({}, status=status.HTTP_200_OK)
    

    def post(self, request, format=None):
        serializer = PDLocationSerializer2(data=request.data)
        if serializer.is_valid():
            user= serializer.validated_data['user']
            try:
                user = CustomUsers.objects.get(id=user.id)
            except CustomUsers.DoesNotExist:
                return Response({"error": "User does not exist."}, status=status.HTTP_400_BAD_REQUEST)
            pd_location = serializer.save()
            user.location = pd_location
            user.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def patch(self, request, pk, format=None):
        try:
            user = CustomUsers.objects.get(pk=pk)
        except PDLocation.DoesNotExist:
            return Response({"error": "PDLocation not found"}, status=status.HTTP_404_NOT_FOUND)
        driver_id = request.data.get('driver_id')
        print(driver_id)
        driver = CustomUsers.objects.get(id=driver_id)
        print(driver)
        serializer = PDLocationSerializer2(user.location, data=request.data, partial=True)
        if serializer.is_valid():
            adriver = driver_id
            serializer.save(acpted_driver = adriver)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



# class NearbyDriversAPIView(generics.ListAPIView):
#     serializer_class = CustomUserSerializer
#     def get(self, request, user_id):
#         user = CustomUsers.objects.get(id=user_id)
#         user_location = user.location
#         # print(user.is_accepted)
#         if user.is_accepted == "False":
#             print("sdfasdfadsfASDFVASDFASDFa")
#             user_latitude = float(user_location.pickup_latitude)
#             user_longitude = float(user_location.pickup_longitude)
#             nearby_drivers = self.get_queryset()
#             updated_location_ids = []
#             for driver in nearby_drivers:
#                 print(driver.location)
#                 driver_latitude = float(driver.location.pickup_latitude)
#                 driver_longitude = float(driver.location.pickup_longitude)
#                 distance = self.calculate_distance(user_latitude, user_longitude, driver_latitude, driver_longitude) 
#                 if distance <= 100:
#                     updated_location_ids.append(driver.id)
#             return Response({"message": str(updated_location_ids)})
#         else:
#             # pass
#             print(user.is_accepted)
#             driver = CustomUsers.objects.get(username=user.is_accepted)
#             print(driver.id)
#             return Response({"driver": driver.id})
#     def calculate_distance(self, lat1, lon1, lat2, lon2):
#         point1 = (lat1, lon1)
#         point2 = (lat2, lon2)
#         print(geodesic(point1, point2).kilometers)
#         return geodesic(point1, point2).kilometers

#     def get_queryset(self):
#         nearby_drivers = CustomUsers.objects.filter(user_type='driver')
#         print(nearby_drivers)
#         return nearby_drivers

# class Driveracpted(APIView):
#     def post(self,request):
#         serializer = CustomSerializer(data=request.data)
#         if serializer.is_valid():
#             user_id = request.data.get('user_id')
#             driver_id = request.data.get('driver_id')

#             user = CustomUsers.objects.get(id=2)
#             driver = CustomUsers.objects.get(id=4)
#             user.is_accepted = driver.username
#             # user.is_accepted = True  # Assuming is_accepted is a boolean field
#             user.save()  # Save only the is_accepted field
        
#             return Response({"message": "Driver accepted successfully"}, status=status.HTTP_200_OK)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
# class NearbyDriversAPIView(generics.ListAPIView):
#     serializer_class = CustomUserSerializer

#     def get(self, request, user_id):
#         user = CustomUsers.objects.get(id=user_id)
#         user_location = user.location
#         user_latitude = float(user_location.pickup_latitude)
#         user_longitude = float(user_location.pickup_longitude)
#         nearby_drivers = self.get_queryset()
#         updated_location_ids = []
#         for driver in nearby_drivers:
#             print(driver.location)
#             driver_latitude = float(driver.location.pickup_latitude)
#             driver_longitude = float(driver.location.pickup_longitude)
#             distance = self.calculate_distance(user_latitude, user_longitude, driver_latitude, driver_longitude) 
#             if distance <= 100:
#                 # address = self.get_address_from_coordinates(driver_latitude, driver_longitude)
#                 # serializer = CustomUserSerializer(driver)
#                 # serializer_data = serializer.data
#                 # serializer_data['loaction_address'] = address
#                 # updated_serializer = CustomUserSerializer(driver, data=serializer_data, partial=True)                
#                 # if updated_serializer.is_valid():
#                 #     if address is None:
#                 #         updated_location_ids.append(str(driver.id))
#                 #     else:
#                 #         updated_serializer.save(loacmail.id))
#         return Response({"message": str(updated_location_ids)})
#     def calculate_distance(self, lat1, lon1, lat2, lon2):
#         point1 = (lat1, lon1)
#         point2 = (lat2, lon2)
#         print(geodesic(point1, point2).kilometers)
#         return geodesic(point1, point2).kilometers
#     def get_address_from_coordinates(self, latitude, longitude):
#         geolocator = Nominatim(user_agent="my_geocoder")
#         try:
#             location = geolocator.reverse((latitude, longitude), language='en', timeout=10)
#             return location.address if location else None
#         except Exception as e:
#             print(f"Error: {e}")
#             return None

#     def get_queryset(self):
#         nearby_drivers = CustomUsers.objects.filter(user_type='driver')
#         print(nearby_drivers)
#         return nearby_drivers

@api_view(['GET'])
def get_active_rides(request, user_id):
    if request.method == 'GET':
        # Query active PDLocation objects for the specific user ID with status 1 or 2
        active_rides = PDLocation.objects.filter(user_id=user_id, status__in=[1])

        # Prepare data to be serialized (if needed)
        data = []
        for ride in active_rides:
            ride_data = {
                'id': ride.id,
                'user_id': ride.user_id,
                'current_latitude': float(ride.current_latitude),
                'current_longitude': float(ride.current_longitude),
                'destination_latitude': float(ride.destination_latitude),
                'destination_longitude': float(ride.destination_longitude),
                'destination_address': ride.destination_address,
                'pickup_address': ride.pickup_address,
                'people_count': ride.people_count,
                'pickup_time': ride.pickup_time,
                'status': ride.status,
                'acpted_driver': ride.acpted_driver,
            }
            data.append(ride_data)

        # Return data as JSON response
        return JsonResponse(data, safe=False)
    else:
        # Method not allowed
        return JsonResponse({'error': 'Method not allowed'}, status=405)

@api_view(['GET'])
def get_past_rides(request, user_id):
    if request.method == 'GET':
        # Query active PDLocation objects for the specific user ID with status 1 or 2
        active_rides = PDLocation.objects.filter(user_id=user_id, status__in=[3])

        # Prepare data to be serialized (if needed)
        data = []
        for ride in active_rides:
            ride_data = {
                'id': ride.id,
                'user_id': ride.user_id,
                'current_latitude': float(ride.current_latitude),
                'current_longitude': float(ride.current_longitude),
                'destination_latitude': float(ride.destination_latitude),
                'destination_longitude': float(ride.destination_longitude),
                'destination_address': ride.destination_address,
                'pickup_address': ride.pickup_address,
                'people_count': ride.people_count,
                'pickup_time': ride.pickup_time,
                'status': ride.status,
                'acpted_driver': ride.acpted_driver,
            }
            data.append(ride_data)

        # Return data as JSON response
        return JsonResponse(data, safe=False)
    else:
        # Method not allowed
        return JsonResponse({'error': 'Method not allowed'}, status=405)

@api_view(['GET'])
def get_driver_rides(request, driver_id):
    if request.method == 'GET':
        # Query active PDLocation objects for the specific driver ID with status 3
        active_rides = PDLocation.objects.filter(acpted_driver=driver_id, status=3)

        # Prepare data to be serialized
        data = []
        for ride in active_rides:
            try:
                # Access the CustomUser associated with the ride and retrieve name and phone number
                custom_user = CustomUsers.objects.get(pk=ride.user_id)
                ride_data = {
                    'id': ride.id,
                    'user_id': ride.user_id,
                    'username': custom_user.username,  # Assuming 'name' is the field name in the CustomUsers model
                    'phone_number': custom_user.phone_number,  # Assuming 'phone_number' is the field name in the CustomUsers model
                    'current_latitude': float(ride.current_latitude),
                    'current_longitude': float(ride.current_longitude),
                    'destination_latitude': float(ride.destination_latitude),
                    'destination_longitude': float(ride.destination_longitude),
                    'destination_address': ride.destination_address,
                    'pickup_address': ride.pickup_address,
                    'people_count': ride.people_count,
                    'pickup_time': ride.pickup_time,
                    'status': ride.status,
                    'acpted_driver': ride.acpted_driver,
                }
                data.append(ride_data)
            except CustomUsers.DoesNotExist:
                pass  # Handle the case when the CustomUser associated with the ride does not exist

        # Return data as JSON response
        return JsonResponse(data, safe=False)
    else:
        # Method not allowed
        return JsonResponse({'error': 'Method not allowed'}, status=405)

@api_view(['GET'])
def get_driveraccepted_rides(request, user_id):
    if request.method == 'GET':
        # Query active PDLocation objects for the specific user ID with status 1 or 2
        active_rides = PDLocation.objects.filter(user_id=user_id, status__in=[2])

        # Prepare data to be serialized (if needed)
        data = []
        for ride in active_rides:
            ride_data = {
                'id': ride.id,
                'user_id': ride.user_id,
                'current_latitude': float(ride.current_latitude),
                'current_longitude': float(ride.current_longitude),
                'destination_latitude': float(ride.destination_latitude),
                'destination_longitude': float(ride.destination_longitude),
                'destination_address': ride.destination_address,
                'pickup_address': ride.pickup_address,
                'people_count': ride.people_count,
                'pickup_time': ride.pickup_time,
                'status': ride.status,
                'acpted_driver': ride.acpted_driver,
            }
            data.append(ride_data)

        # Return data as JSON response
        return JsonResponse(data, safe=False)
    else:
        # Method not allowed
        return JsonResponse({'error': 'Method not allowed'}, status=405)

@api_view(['GET'])
def ended_rides(request, user_id):
    if request.method == 'GET':
        # Query active PDLocation objects for the specific user ID with status 1 or 2
        active_rides = PDLocation.objects.filter(user_id=user_id, status__in=[4])

        # Prepare data to be serialized (if needed)
        data = []
        for ride in active_rides:
            ride_data = {
                'id': ride.id,
                'user_id': ride.user_id,
                'current_latitude': float(ride.current_latitude),
                'current_longitude': float(ride.current_longitude),
                'destination_latitude': float(ride.destination_latitude),
                'destination_longitude': float(ride.destination_longitude),
                'destination_address': ride.destination_address,
                'pickup_address': ride.pickup_address,
                'people_count': ride.people_count,
                'pickup_time': ride.pickup_time,
                'status': ride.status,
                'acpted_driver': ride.acpted_driver,
            }
            data.append(ride_data)

        # Return data as JSON response
        return JsonResponse(data, safe=False)
    else:
        # Method not allowed
        return JsonResponse({'error': 'Method not allowed'}, status=405)

@api_view(['PATCH'])
def end_ride(request, ride_id):
    if request.method == 'PATCH':
        try:
            # Find the ride object by ID
            ride = PDLocation.objects.get(id=ride_id)

            # Update the status to 4 (completed)
            ride.status = 4
            ride.save()

            # Return success response
            return JsonResponse({'message': 'Ride ended successfully'}, status=200)
        except PDLocation.DoesNotExist:
            # If the ride with the provided ID doesn't exist, return 404 Not Found
            return JsonResponse({'error': 'Ride not found'}, status=404)
    else:
        # Method not allowed
        return JsonResponse({'error': 'Method not allowed'}, status=405)