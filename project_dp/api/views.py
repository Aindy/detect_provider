from rest_framework.views import APIView
from rest_framework.response import Response
from telecom.models import PhoneNumber
from api.serializers import PhoneNumberSerializer

class PhoneNumberInfo(APIView):
    def get(self, request, msisdn):
        try:
            number_int = int(msisdn[-7:])
            phone_number = PhoneNumber.objects.filter(start_range__lte=number_int, end_range__gte=number_int).first()
            if phone_number:
                serializer = PhoneNumberSerializer(phone_number)
                return Response(serializer.data)
            else:
                return Response({'error': 'Номер не найден'}, status=status.HTTP_404_NOT_FOUND)
        except ValueError:
            return Response({'error': 'Неверный формат номера'}, status=status.HTTP_400_BAD_REQUEST)
