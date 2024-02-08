from django.urls import path
from api.views import PhoneNumberInfo

urlpatterns = [
    path('phone_number/<str:msisdn>/', PhoneNumberInfo.as_view(), name='phone-number-info'),
]