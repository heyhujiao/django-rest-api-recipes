from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

CREATE_USER_URL = reverse('users:create')
TOKEN_URL = reverse('users:token')


def create_user(**params):
    return get_user_model().objects.create_user(**params)


class PublicUserApiTests(TestCase):
    """
    Test the user API (public)
    """

    def setUp(self):
        self.client = APIClient()

    def test_create_valid_user_success(self):
        """
        test creating user with valid payload is successful
        :return:
        """
        payload = {
            'email': 'lalal@bigbang.com',
            'password': 'hihihihihih',
            'name': 'Wee'
        }
        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(**res.data)
        self.assertTrue(user.check_password(payload['password']))
        self.assertNotIn('password', res.data)

    def test_user_exists(self):
        """
        test creating a user that already exists fails
        :return:
        """
        payload = {
            'email': 'lalal@bigbang.com',
            'password': 'hihihihihih',
            'name': 'Wee'
        }
        create_user(**payload)

        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short(self):
        """
        test that the password must be at least 5 characters
        :return:
        """
        payload = {
            'email': 'lalal@bigbang.com',
            'password': 'w',
            'name': 'Wee'
        }

        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        user_exists = get_user_model().objects.filter(
            email=payload['email']
        ).exists()
        self.assertFalse(user_exists)

    """
    Token created API
    """

    def test_create_token_for_user(self):
        """
        test that a token is created for user
        :return:
        """

        payload = {
            'email': 'test@example.com',
            'password': 'teasd123123'
        }
        create_user(**payload)

        res = self.client.post(TOKEN_URL, payload)

        self.assertIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_token_invalid_credentials(self):
        """
        test that no token is created if the credentials given are not valid
        :return:
        """
        create_user(email='test@example.com',
                    password='teasd123123')
        payload = {
            'email': 'test@example.com',
            'password': 'nopeddd'
        }
        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_no_user(self):
        """
        test that token is not created if user does not exist
        :return:
        """
        payload = {
            'email': 'test@example.com',
            'password': 'nopeddd'
        }
        res = self.client.post(TOKEN_URL, payload)
        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_missing_field(self):
        """
        test that email and password are required
        :return:
        """

        res = self.client.post(
            TOKEN_URL,
            {"email": 'asdas@das.com', "password": 'hiyahshdas'}
        )
        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
