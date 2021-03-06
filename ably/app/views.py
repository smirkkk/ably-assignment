from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny

from .serializers import LoginSerializer, PhoneSerializer, CertifyPhoneSerializer, SignupSerializer, LoginSerializer, UserSerializer, PasswordSerializer


def get_jwt_token(data) -> str:
    """
    로그인
    """
    serializer = LoginSerializer(data=data)

    if serializer.is_valid(raise_exception=True):
        token = serializer.validated_data
        return token
    else:
        return None


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
        else:
            return Response(False)


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
            return Response(True)
        else:
            return Response(False)
        


class UserView(APIView):
    """
    get : 현재 로그인한 유저 정보 조회
    post : 회원가입
    """

    def get_permissions(self):
        # 메소드에 따라 permission 구분
        if self.request.method == "GET":
            return [IsAuthenticated()]
        elif self.request.method == "POST":
            return [AllowAny()]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)

    def post(self, request):
        phone = request.session.get('phone', None)
        try:
            data = request.data.dict()
        except AttributeError:
            data = request.data

        data['phone'] = phone

        serializer = SignupSerializer(data=data)

        if serializer.is_valid(raise_exception=True):
            serializer.save()

            # 방금 가입한 정보로 로그인
            token = get_jwt_token(
                dict(username=data['username'], password=data['password']))
            del request.session['phone']  # 세션에서 전화번호 삭제

            return Response(dict(token=token))
        else:
            return Response(False)


class LoginView(APIView):
    """
    로그인
    """
    permission_classes = (AllowAny, )

    def post(self, request):
        token = get_jwt_token(data=request.data)
        return Response(dict(token=token))


class ResetPasswordView(APIView):
    """
    비밀번호 재설정
    """

    permission_classes = (AllowAny, )

    def post(self, request):
        phone = request.session.get('phone', None)
        try:
            data = request.data.dict()
        except AttributeError:
            data = request.data

        data['phone'] = phone

        serializer = PasswordSerializer(data=data)

        if serializer.is_valid(raise_exception=True):
            serializer.save()

            del request.session['phone']  # 세션에서 전화번호 삭제

            return Response(True)
        else:
            return Response(False)
