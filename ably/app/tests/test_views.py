from django.test import TestCase

from app.models import User

test_phone = '01012345678'
test_nickname = 'nickname'
test_first_name = 'First'
test_last_name = 'Last'
test_username = 'username1'
test_password = 'password1'
test_new_password = 'password2'
test_email = 'test2@test.com'


class SignupTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        user = User.objects.create(
            username='test', email='test@test.com', phone='01011111111', nickname='nickname')
        user.set_password('password')
        user.save()

    def test_phone_certify_fail_by_duplicated(self):
        response = self.client.post("/users/pins", {
            'phone': '01011111111'
        }, content_type='application/json')

        self.assertEqual(response.status_code, 200)

        response = self.client.post("/users/phones", {
            'phone': '01011111111',
            'pin': '123456'
        }, content_type='application/json')

        self.assertEqual(response.status_code, 400)

    def test_signup_and_user_data(self):
        response = self.client.post("/users/pins", {
            'phone': test_phone
        }, content_type='application/json')

        self.assertEqual(response.status_code, 200)

        response = self.client.post("/users/phones", {
            'phone': test_phone,
            'pin': '123456'
        }, content_type='application/json')

        self.assertEqual(response.status_code, 200)

        response = self.client.post("/users", {
            'phone': test_phone,
            'nickname': test_nickname,
            'first_name': test_first_name,
            'last_name': test_last_name,
            'username': test_username,
            'password': test_password,
            'password2': test_password,
            'email': test_email
        }, content_type='application/json')

        self.assertEqual(response.status_code, 200)

        token = response.json()['token']
        header = {'HTTP_AUTHORIZATION': f'jwt {token}'}

        response = self.client.get("/users", **header)
        self.assertEqual(response.status_code, 200)

        user_data = response.json()

        self.assertEqual(user_data['phone'], test_phone)
        self.assertEqual(user_data['email'], test_email)
        self.assertEqual(user_data['username'], test_username)
        self.assertEqual(user_data['nickname'], test_nickname)
        self.assertEqual(user_data['first_name'], test_first_name)
        self.assertEqual(user_data['last_name'], test_last_name)

    def test_get_user_data_without_token(self):
        response = self.client.get("/users")
        self.assertEqual(response.status_code, 401)


class LoginTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        user = User.objects.create(
            username=test_username, email=test_email, phone=test_phone)
        user.set_password(test_password)
        user.save()

    def test_login_by_username(self):
        response = self.client.post("/users/login", {
            'username': test_username,
            'password': test_password
        }, content_type='application/json')

        self.assertEqual(response.status_code, 200)

    def test_login_by_phone(self):
        response = self.client.post("/users/login", {
            'phone': test_phone,
            'password': test_password
        }, content_type='application/json')

        self.assertEqual(response.status_code, 200)

    def test_login_by_email(self):
        response = self.client.post("/users/login", {
            'email': test_email,
            'password': test_password
        }, content_type='application/json')

        self.assertEqual(response.status_code, 200)

    def test_login_failed_by_wrong_password(self):
        response = self.client.post("/users/login", {
            'username': test_email,
            'password': ''
        }, content_type='application/json')

        self.assertEqual(response.status_code, 400)

    def test_login_with_multiple_key(self):
        response = self.client.post("/users/login", {
            'username': test_username,
            'email': test_email,
            # 'phone': test_phone,
            'password': ''
        }, content_type='application/json')

        self.assertEqual(response.status_code, 400)


class ResetPasswordTest(TestCase):
    def reset_password(self):
        self.client.post("/users/phones", {
            'phone': test_phone,
            'pin': '123456',
            'unique_only': False
        }, content_type='application/json')

        self.client.post("/users/passwords", {
            'password': test_new_password,
            'password2': test_new_password
        }, content_type='application/json')

    @classmethod
    def setUpTestData(cls):
        user = User.objects.create(
            username=test_username, email=test_email, phone=test_phone)
        user.set_password(test_password)
        user.save()

    def test_phone_certify_fail_by_unknown_phone_number(self):
        response = self.client.post("/users/pins", {
            'phone': '01011111111'
        }, content_type='application/json')

        self.assertEqual(response.status_code, 200)

        response = self.client.post("/users/phones", {
            'phone': '01011111111',
            'pin': '123456',
            'unique_only': False
        }, content_type='application/json')

        self.assertEqual(response.status_code, 400)

    def test_reset_password(self):
        response = self.client.post("/users/pins", {
            'phone': test_phone
        }, content_type='application/json')

        self.assertEqual(response.status_code, 200)

        response = self.client.post("/users/phones", {
            'phone': test_phone,
            'pin': '123456',
            'unique_only': False
        }, content_type='application/json')

        self.assertEqual(response.status_code, 200)

        response = self.client.post("/users/passwords", {
            'password': test_new_password,
            'password2': test_new_password
        }, content_type='application/json')

        self.assertEqual(response.status_code, 200)

    def test_login_with_new_password(self):
        self.reset_password()

        response = self.client.post("/users/login", {
            'phone': test_phone,
            'password': test_new_password
        }, content_type='application/json')

        self.assertEqual(response.status_code, 200)
