from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from .serializers import PhoneSerializer, CertifyPhoneSerializer


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
            # 세션에 저장된 전화번호가 있다면 삭제
            try:
                del request.session['phone']
            except KeyError:
                pass

            self.send_pin(phone)
            return Response(True)


class CertifyPhoneView(APIView):
    """
    전화번호 인증
    """
    permission_classes = (AllowAny, )

    def post(self, request):
        serializer = CertifyPhoneSerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            phone = request.data.get('phone', None)
            request.session['phone'] = phone  # 인증된 전화번호 세션에 저장
            return Response()
