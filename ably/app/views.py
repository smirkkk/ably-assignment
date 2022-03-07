from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from .serializers import PhoneSerializer


class SendPinView(APIView):
    """
    인증번호 발송
    """
    permission_classes = (AllowAny, )

    def send_pin(self, phone):
        print("인증번호 발송")
        
        return True

    def post(self, request):
        phone = request.data.get('phone', None)
        serializer = PhoneSerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            self.send_pin(phone)
            return Response(True)
