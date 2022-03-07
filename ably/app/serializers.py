import re
from rest_framework import serializers

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
