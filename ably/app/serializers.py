import re
from rest_framework import serializers
from .models import User


def is_phone_unique(phone):
    """
    전화번호 중복 확인
    """

    if User.objects.filter(phone=phone).exists():
        return False
    else:
        return True


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

    def certify_pin(self, phone, pin):
        """
        전화번호 인증
        """

        # 인증

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
