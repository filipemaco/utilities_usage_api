from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase

from utils.tests_helpers import request_factory

from .viewsets import UserViewSet

User = get_user_model()


class UserViewSetTests(APITestCase):

    def setUp(self):
        User.objects.create_user(
            name='Robert',
            email='robert@email.com',
            password='robert'
        )
        User.objects.create_user(
            name='Rose',
            email='rose@email.com',
            password='rose'
        )
        User.objects.create_superuser(
            name='Admin',
            email='admin@email.com',
            password='admin'
        )

    def _base_for_patch_put_and_delete_test(self):
        user = User.objects.get(email='rose@email.com')
        pk = user.id
        url = reverse('users:users-detail', kwargs={'pk': pk})
        return url, user, pk

    def test_get_users_with_admin(self):
        url = reverse('users:users-list')
        user = User.objects.get(email='admin@email.com')
        response = request_factory(UserViewSet, user, url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('count'), 3)

    def test_get_users_with_normal_user(self):
        url = reverse('users:users-list')
        user = User.objects.get(email='rose@email.com')
        response = request_factory(UserViewSet, user, url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_user_with_success(self):
        url, user, pk = self._base_for_patch_put_and_delete_test()
        response = request_factory(
            UserViewSet, user, url, 'delete', pk=pk)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(User.objects.all().count(), 2)
        self.assertEqual(
            User.objects.filter(email='rose@email.com').count(),
            0
        )

    def test_change_name_of_user_with_success(self):
        url, user, pk = self._base_for_patch_put_and_delete_test()
        data = {
            'name': 'Maria',
        }
        response = request_factory(
            UserViewSet, user, url, 'patch', data, pk)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        user = User.objects.get(email='rose@email.com')
        self.assertEqual(user.name, data['name'])

    def test_changes_in_user_with_success(self):
        url, user, pk = self._base_for_patch_put_and_delete_test()
        data = {
            'name': 'Jose',
            'password': 'Random',
            'email': 'jose@test.com'
        }
        response = request_factory(
            UserViewSet, user, url, 'put', data, pk)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        user = User.objects.get(email='jose@test.com')
        self.assertEqual(user.name, data['name'])
