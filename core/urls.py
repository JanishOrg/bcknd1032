# core/urls.py

from django.urls import path
from .views import *

urlpatterns = [
    # path('driver/', CustomUserListCreateView.as_view(), name='customuser-list-create'),
    # path('driver/<int:pk>/', CustomUserDetailView.as_view(), name='customuser-detail'),
    path('login/', LoginAPIView.as_view(), name='login'),
    path('logout/', LogoutAPIView.as_view(), name='logout'),
    path('search/<str:username>/', Search.as_view(), name='logout'),
    path('user_type/<str:user_type>/', UserTypeListView.as_view(), name='user-type-list'),
    path('driver/', CustomUserAPIView.as_view(), name='custom-users-list-create'),
    path('driver/<int:pk>/', CustomUserAPIView.as_view(), name='custom-users-detail'),
    path('forgot-password/', ForgotPasswordView.as_view(), name='forgot-password'),
    path('update-password/', PasswordUpdateView.as_view(), name='update-password'),
    path('location/', PDLocationCreateAPIView.as_view(), name='location'),
    path('testoo/<int:id>/', testoo.as_view(), name='dlaa'),
    path('change-password/', ChangePasswordView.as_view(), name='change-password'),
    path('get-nearby-user/<int:pk>/', PDLocationAPIView.as_view(), name='get-nearby-user'),
    path('get-acceptedby-user/<int:pk>/', dfd.as_view(), name='get-acceptedby-use'),
    path('update-from-user/<int:pk>/', PDLocationDetailAPIView.as_view(), name='update-from-user'),
    path('create-booking-data/', PDLocationAPIView2.as_view(), name='create-booking-data'),
    path('accpet-from-driver/<int:pk>', PDLocationAPIView2.as_view(), name='accpet-from-driver'),
    path('get-current-rides/<int:user_id>/', get_active_rides, name='get_active_rides'),
    path('get-active-rides/<int:user_id>/', get_past_rides ,name='get_past_rides'),
    path('get-driver-rides/<int:driver_id>', get_driver_rides, name='get_driver_rides'),
    path('get-driveraccepted-rides/<int:user_id>', get_driveraccepted_rides, name='get_driveraccepted_rides'),
    path('get-ended-rides/<int:user_id>',ended_rides,name='endedrides'),
    path('end-ride/<int:ride_id>',end_ride,name="end_ride"),
]
