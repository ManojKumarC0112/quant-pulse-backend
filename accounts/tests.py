from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth import get_user_model

User = get_user_model()

class AuthAndRBACLogicTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='trader1', password='securepassword123', role='USER')
        self.admin = User.objects.create_user(username='admin1', password='adminpassword123', role='ADMIN')

    def test_successful_login_returns_jwt(self):
        """Test that valid credentials return access and refresh tokens."""
        url = reverse('auth_login') # ensure this matches urls.py name 'auth_login'
        response = self.client.post(url, {'username': 'trader1', 'password': 'securepassword123'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_failed_login_handles_gracefully(self):
        """Test that invalid credentials return standard 400 errors, not 500 crashes."""
        url = reverse('auth_login')
        response = self.client.post(url, {'username': 'trader1', 'password': 'wrongpassword'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
