from django.urls import path, include
from telecom.views import index

urlpatterns = [
    path('api/', include('api.urls')),
    path('', index, name='index'),
]
