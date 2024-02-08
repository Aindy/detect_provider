from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import re
import logging
from telecom.models import PhoneNumber
from api.serializers import PhoneNumberSerializer

logger = logging.getLogger(__name__)


class PhoneNumberInfo(APIView):
    def get(self, request, msisdn):
        if not re.match(r'^\d{11}$', msisdn):
            return Response({'error': 'Номер должен состоять из 11 цифр'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            number_int = int(msisdn[-7:])
            phone_number = PhoneNumber.objects.filter(start_range__lte=number_int, end_range__gte=number_int).first()
            if phone_number:
                logger.info(f"Проверяемый номер: {number_int}")
                serializer = PhoneNumberSerializer(phone_number)
                return Response(serializer.data)
            else:
                return Response({'error': 'Номер не найден'}, status=status.HTTP_404_NOT_FOUND)
        except ValueError:
            return Response({'error': 'Неверный формат номера'}, status=status.HTTP_400_BAD_REQUEST)
