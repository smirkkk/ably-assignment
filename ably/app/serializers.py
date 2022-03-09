import re
from typing import Union

from django.db.models import Q
from django.core.validators import RegexValidator
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from rest_framework_jwt.settings import api_settings

from .models import User

username_validator = RegexValidator(
    "^(?=.*[a-zA-Z])(?=.*\d)[a-zA-Z\d]{6,12}$", '아이디는 영어, 숫자 포함 6글자 이상 12글자 미만이어야 합니다.')
password_validator = RegexValidator(
    "^(?=.*[a-zA-Z])(?=.*\d)[a-zA-Z\d]{8,}$", '비밀번호는 영어, 숫자를 섞어 8글자 이상이어야 합니다.')


def is_phone_unique(phone: str) -> bool:
    """
    전화번호 중복 확인
    """

    if User.objects.filter(phone=phone).exists():
        return False
    else:
        return True


def authenticate(**kwargs) -> Union[User, None]:
    """
    로그인

    kwargs : (아이디 or 이메일 or 전화번호), 비밀번호
    """

    # unique한 필드 list와 사용자 입력값의 교집합
    fields = ["username", "email", "phone"]
    intersection = list(set(fields).intersection(kwargs.keys()))

    if len(intersection) != 1:
        raise serializers.ValidationError("아이디, 이메일, 전화번호 중에서 한 가지를 선택해주세요.")

    try:
        user = User.objects.get(
            Q(username=kwargs.get('username', "")) |
            Q(email=kwargs.get('email', "")) |
            Q(phone=kwargs.get('phone', ""))
        )
    except User.DoesNotExist:
        raise serializers.ValidationError("입력값을 확인해주세요.")

    except User.MultipleObjectsReturned:
        raise serializers.ValidationError("다른 항목으로 시도해주세요.")

    else:
        if user.check_password(kwargs['password']):
            return user
        else:
            return None


class PhoneSerializer(serializers.Serializer):
    """
    전화번호 형식 확인
    """

    phone = serializers.CharField(required=True, max_length=11)

    def validate_phone(self, phone):
        # 01로 시작하는 숫자 10 ~ 11자리
        phone_pattern = "^(01)([0-9]{8,9})\d$"

        if re.match(phone_pattern, phone):
            return True
        else:
            raise serializers.ValidationError({
                'phone': '-을 제외한 정확한 전화번호를 입력해주세요.'
            })


class CertifyPhoneSerializer(serializers.Serializer):
    """
    전화번호 인증
    """

    phone = serializers.CharField(required=True, max_length=11)
    pin = serializers.CharField(required=True, max_length=6)

    # True = 중복되지 않는 전화번호만
    # False = 중복되는(존재하는) 전화번호만
    unique_only = serializers.BooleanField(default=True)

    def certify_pin(self, phone: str, pin: str):
        print("인증")

        return True

    def validate(self, data):
        phone = data.get('phone', None)
        pin = data.get('pin', None)
        unique_only = data.get('unique_only', True)

        if not self.certify_pin(phone, pin):
            raise serializers.ValidationError({
                'pin': '인증번호가 올바르지 않습니다.'
            })

        if unique_only and not is_phone_unique(phone=phone):
            raise serializers.ValidationError({
                'phone': '중복된 전화번호입니다.'
            })

        elif not unique_only and is_phone_unique(phone=phone):
            raise serializers.ValidationError({
                'phone': '존재하지 않는 전화번호입니다.'
            })

        return True


class SignupSerializer(serializers.Serializer):
    """
    회원가입
    """

    email = serializers.EmailField(required=True, validators=[UniqueValidator(
        queryset=User.objects.all(), message="중복된 이메일입니다.")])
    username = serializers.CharField(required=True, validators=[
                                     username_validator, UniqueValidator(queryset=User.objects.all(), message="중복된 아이디입니다.")])
    password = serializers.CharField(
        required=True, validators=[password_validator])
    password2 = serializers.CharField(required=True)
    phone = serializers.CharField(required=True, max_length=11, validators=[
                                  UniqueValidator(queryset=User.objects.all(), message="중복된 전화번호입니다.")])
    nickname = serializers.CharField(required=True, max_length=20)

    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)

    def validate(self, data):
        password = data.get("password", None)
        password2 = data.get("password2", None)

        if password != password2:
            raise serializers.ValidationError({
                'password2': '비밀번호가 일치하지 않습니다.'
            })

        return data

    def create(self, validated_data):
        user = User.objects.create(
            email=validated_data['email'],
            username=validated_data['username'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            phone=validated_data['phone'],
            nickname=validated_data['nickname']
        )

        user.set_password(validated_data['password'])

        user.save()
        return user


JWT_PAYLOAD_HANDLER = api_settings.JWT_PAYLOAD_HANDLER
JWT_ENCODE_HANDLER = api_settings.JWT_ENCODE_HANDLER


class LoginSerializer(serializers.Serializer):
    """
    로그인
    """

    username = serializers.CharField(required=False)
    phone = serializers.CharField(required=False)
    email = serializers.CharField(required=False)
    password = serializers.CharField(required=True, write_only=True)
    token = serializers.CharField(max_length=255, read_only=True)

    def validate(self, data):
        user = authenticate(**data)

        if user:
            # 로그인 성공한 경우 JWT 생성
            payload = JWT_PAYLOAD_HANDLER(user)
            token = JWT_ENCODE_HANDLER(payload)

            return token
        else:
            raise serializers.ValidationError("입력값을 확인해주세요.")


class UserSerializer(serializers.ModelSerializer):
    """
    회원 정보 조회
    """
    class Meta:
        model = User
        fields = ["username", "email", "first_name", "last_name", "phone"]
