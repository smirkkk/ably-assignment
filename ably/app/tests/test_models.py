from django.test import TestCase
from app.models import User


class UserModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        user = User.objects.create(
            username='test', password='test', email='test@test.com', phone='01011111111', nickname='nickname')
        user.set_password('password')
