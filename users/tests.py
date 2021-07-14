from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from faker import Faker


class UserSignUpTestCase(APITestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.signup_url = reverse('signup')
        cls.signin_url = reverse('token_obtain_pair')
        cls.token_refresh_url = reverse('token_refresh')
        cls.client = APIClient()
        cls.fake = Faker()
        cls.existing_user_data = {
            "username": "testuser",
            "password": "123456"
        }
        res = cls.client.post(cls.signup_url, cls.existing_user_data, format="json")
        cls.existing_user_refresh_data = {'refresh': res.data['tokens']['refresh']}

        cls.new_user_data = {
            "username": cls.fake.email(),
            "password": cls.fake.password(
                length=8,
                special_chars=True,
                digits=True,
                upper_case=True,
                lower_case=True,
            )
        }

    def test_user_cannot_signup_with_no_data(self):
        res = self.client.post(self.signup_url)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            str(res.data['detail']['username'][0]),
            'This field is required.',
        )
        self.assertEqual(
            str(res.data['detail']['password'][0]),
            'This field is required.',
        )

    def test_user_can_signup(self):
        res = self.client.post(self.signup_url, self.new_user_data, format="json")
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(res.data['username'], self.new_user_data['username'])
        self.assertIn('tokens', res.data)

    def test_user_already_exist_while_signup(self):
        res = self.client.post(self.signup_url, self.existing_user_data, format="json")
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            str(res.data['detail']['username'][0]),
            'A user with that username already exists.',
        )

    def test_user_can_signin(self):
        res = self.client.post(self.signin_url, self.existing_user_data, format="json")
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn('refresh', res.data)
        self.assertIn('access', res.data)

    def test_user_cannot_signin_with_bad_credentials(self):
        wrong_credentials = {
            'username': "doesntexist",
            'password': "doesntexist"
        }
        res = self.client.post(self.signin_url, wrong_credentials, format="json")
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(
            str(res.data['detail']),
            'No active account found with the given credentials',
        )

    def test_user_can_refresh_token(self):
        res = self.client.post(self.token_refresh_url, self.existing_user_refresh_data, format="json")
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn('access', res.data)
