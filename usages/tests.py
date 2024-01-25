import json
import pytz

from datetime import datetime

from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils import timezone

from rest_framework import status
from rest_framework.test import APITestCase

from utils.tests_helpers import request_factory

from .utils import get_calculated_emissions
from .models import Usage, UsageType
from .viewsets import UsageTypeViewSet, UsageViewSet
from .tests_utils import (create_super_and_normal_user, create_usage_types,
                          create_usage_for_users)

User = get_user_model()


class UsageTypeTests(APITestCase):

    def setUp(self):
        create_super_and_normal_user()
        create_usage_types()

    def _base_for_patch_put_and_delete_test(self):
        water_usage = UsageType.objects.get(name='water')
        pk = water_usage.id
        url = reverse('usage:usage_types-detail', kwargs={'pk': pk})
        user = User.objects.get(email='admin@example.com')
        return url, user, pk

    def test_get_usage_type_list(self):
        url = reverse('usage:usage_types-list')
        user = User.objects.get(email='not_admin@example.com')
        response = request_factory(UsageTypeViewSet, user, url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('count'), 3)
        self.assertEqual(response.data.get('results')[0]['name'], 'heating')
        self.assertEqual(response.data.get('results')[0]['factor'], 32.2)
        self.assertEqual(response.data.get('results')[-1]['name'], 'heating')
        self.assertEqual(response.data.get('results')[-1]['factor'], 10)

    def test_get_usage_type_list_filter_by_name_and_sorted_by_factor(self):
        url = reverse('usage:usage_types-list')
        filter_and_sort = '?name__icontains=heat&ordering=factor'
        user = User.objects.get(email='not_admin@example.com')
        response = request_factory(
            UsageTypeViewSet, user, f'{url}{filter_and_sort}')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('count'), 2)
        self.assertEqual(response.data.get('results')[1]['name'], 'heating')
        self.assertEqual(response.data.get('results')[1]['factor'], 32.2)

        filter_and_sort = '?name=heating&ordering=-factor'
        response = request_factory(
            UsageTypeViewSet, user, f'{url}{filter_and_sort}')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('count'), 2)
        self.assertEqual(response.data.get('results')[1]['name'], 'heating')
        self.assertEqual(response.data.get('results')[1]['factor'], 10)

    def test_create_usage_type_with_admin_user_with_success(self):
        url = reverse('usage:usage_types-list')
        data = {
            'name': 'electricity',
            'unit': 'kwh',
            'factor': 2.8
        }
        user = User.objects.get(email='admin@example.com')
        response = request_factory(
            UsageTypeViewSet, user, url, 'post', data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(UsageType.objects.all().count(), 4)
        self.assertEqual(
            UsageType.objects.filter(name='electricity', unit='kwh').count(),
            1
        )

        response = request_factory(UsageTypeViewSet, user, url)
        response = request_factory(
            UsageTypeViewSet, user, url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.get('count'), 4)

    def test_create_usage_type_without_permissions(self):
        url = reverse('usage:usage_types-list')
        data = {
            'name': 'electricity',
            'unit': 'wh',
            'factor': 0.28
        }
        user = User.objects.get(email='not_admin@example.com')
        response = request_factory(
            UsageTypeViewSet, user, url, 'post', data)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(UsageType.objects.all().count(), 3)

    def test_delete_usage_type_with_admin_user_with_success(self):
        url, user, pk = self._base_for_patch_put_and_delete_test()
        response = request_factory(
            UsageTypeViewSet, user, url, 'delete', pk=pk)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(UsageType.objects.all().count(), 2)
        self.assertEqual(
            UsageType.objects.filter(name='water').count(),
            0
        )

    def test_put_usage_type_with_admin_user_with_success(self):
        url, user, pk = self._base_for_patch_put_and_delete_test()
        data = {
            'name': 'gas',
            'unit': 'kwh',
            'factor': 15.25,
        }
        response = request_factory(
            UsageTypeViewSet, user, url, 'put', data, pk)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        water_usage = UsageType.objects.get(pk=pk)

        self.assertEqual(water_usage.name, data['name'])
        self.assertEqual(water_usage.unit, data['unit'])
        self.assertEqual(water_usage.factor, data['factor'])

    def test_patch_usage_type_with_admin_user_with_success(self):
        url, user, pk = self._base_for_patch_put_and_delete_test()
        data = {'name': 'gas'}
        response = request_factory(
            UsageTypeViewSet, user, url, 'patch', data, pk)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        water_usage = UsageType.objects.get(pk=pk)

        self.assertEqual(water_usage.name, data['name'])


class UsageTests(APITestCase):
    def setUp(self):
        create_super_and_normal_user()
        create_usage_types()
        create_usage_for_users()

    def _base_for_patch_put_and_delete_test(self):
        user = User.objects.get(email=f'filipe@example.com')
        usage = Usage.objects.get(user=user, amount=30)
        pk = usage.pk
        url = reverse('usage:usage_types-detail', kwargs={'pk': pk})
        return url, user, pk

    def test_get_usage_list_for_filipe_user(self):
        url = reverse('usage:usages-list')
        user = User.objects.get(email='filipe@example.com')
        response = request_factory(UsageViewSet, user, url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.get('count'), 5)

    def test_get_usage_list_order_and_calculated_emissions_for_john_user(self):
        url = reverse('usage:usages-list')
        user = User.objects.get(email='john@example.com')
        response = request_factory(UsageViewSet, user, url)
        results = response.data.get('results')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.get('count'), 3)
        self.assertEqual(response.data.get('count'), 3)
        self.assertEqual(
            get_calculated_emissions(53, 26.93),
            results[0].get('calculated_emissions'))
        self.assertEqual(53, results[0].get('amount'))
        self.assertEqual(
            get_calculated_emissions(203, 26.93),
            results[-1].get('calculated_emissions'))
        self.assertEqual(203, results[-1].get('amount'))

    def test_get_usage_list_filter_by_amount_and_order_by_name_for_admin_user(self):
        url = reverse('usage:usages-list')
        filter_and_sort = '?amount__gte=7&amount__lte=55'
        filter_and_sort += '&ordering=usage_type__name'
        user = User.objects.get(email='admin@example.com')
        response = request_factory(
            UsageViewSet, user, f'{url}{filter_and_sort}')
        results = response.data.get('results')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.get('count'), 5)
        self.assertEqual(
            results[0].get('usage_type')['name'],
            'heating'
        )
        self.assertEqual(
            results[-1].get('usage_type')['name'],
            'water'
        )

    def test_get_usage_list_filter_by_date_for_admin_user(self):
        url = reverse('usage:usages-list')
        filter_and_sort = '?usage_at__gte=2021-04-01T00:00:00Z'
        filter_and_sort += '&usage_at__lte=2021-04-30T00:00:00Z'
        user = User.objects.get(email='admin@example.com')
        response = request_factory(
            UsageViewSet, user, f'{url}{filter_and_sort}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.get('count'), 2)

    def test_get_usage_list_with_pagination_for_admin_user(self):
        url = reverse('usage:usages-list')
        filter_and_sort = '?limit=3&offset=4'
        user = User.objects.get(email='admin@example.com')
        response = request_factory(
            UsageViewSet, user, f'{url}{filter_and_sort}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data.get('results')), 3)

    def test_create_usage_with_wrong_units_without_success(self):
        url = reverse('usage:usages-list')
        data = {
            'amount': 150,
            'usage_at': timezone.now(),
            'name': 'heating',
            'unit': 'wdask'
        }
        user = User.objects.get(email='filipe@example.com')
        response = request_factory(
            UsageViewSet, user, url, 'post', data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_usage_with_success(self):
        url = reverse('usage:usages-list')
        amount = 150
        data = {
            'amount': amount,
            'usage_at': timezone.now(),
            'name': 'heating',
            'unit': 'kwh'
        }
        user = User.objects.get(email='filipe@example.com')
        response = request_factory(
            UsageViewSet, user, url, 'post', data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        id = response.data.get('id')
        created_usage = Usage.objects.get(id=id)

        self.assertEqual(created_usage.user, user)
        self.assertEqual(created_usage.amount, amount)
        self.assertEqual(
            created_usage.calculated_emissions,
            get_calculated_emissions(amount, 32.2))

    def test_delete_usage_with_success(self):
        url, user, pk = self._base_for_patch_put_and_delete_test()
        response = request_factory(
            UsageViewSet, user, url, 'delete', pk=pk)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(
            Usage.objects.filter(user=user).all().count(), 4)

    def test_patch_usage_with_success(self):
        url, user, pk = self._base_for_patch_put_and_delete_test()
        data = {'unit': 'kwh'}
        response = request_factory(
            UsageViewSet, user, url, 'patch', data, pk=pk)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        usage = Usage.objects.get(user=user, amount=30)
        self.assertEqual(usage.usage_type.unit, 'kwh')
        self.assertEqual(
            usage.calculated_emissions,
            get_calculated_emissions(usage.amount, 32.2))

    def test_patch_usage_without_permission(self):
        url, user, pk = self._base_for_patch_put_and_delete_test()
        data = {'unit': 'kwh'}
        user = User.objects.get(email='john@example.com')
        response = request_factory(
            UsageViewSet, user, url, 'patch', data, pk=pk)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_put_usage_with_success(self):
        url, user, pk = self._base_for_patch_put_and_delete_test()
        amount = 300
        data = {
            'name': 'heating',
            'unit': 'l',
            'amount': amount,
            'date': datetime(2021, 7, 22, tzinfo=pytz.UTC)
        }
        response = request_factory(
            UsageViewSet, user, url, 'patch', data, pk=pk)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        usage = Usage.objects.get(user=user, amount=amount)

        self.assertEqual(
            usage.calculated_emissions,
            get_calculated_emissions(amount, 10))
