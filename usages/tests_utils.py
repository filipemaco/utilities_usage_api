import pytz

from datetime import datetime

from django.contrib.auth import get_user_model
from django.utils import timezone

from .models import UsageType, Usage
from .utils import get_calculated_emissions

User = get_user_model()


def create_super_and_normal_user():
    User.objects.create_superuser(
        email='admin@example.com',
        name='admin',
        password='admin'
    )
    User.objects.create_user(
        email='not_admin@example.com',
        name='Not Admin',
        password='not_admin',
    )
    User.objects.create_user(
        email='filipe@example.com',
        name='Filipe',
        password='filipe',
    )
    User.objects.create_user(
        email='john@example.com',
        name='John',
        password='john',
    )


def create_usage_types():
    UsageType.objects.bulk_create([
        UsageType(
            name='heating',
            unit='kwh',
            factor=32.2
        ),
        UsageType(
            name='water',
            unit='kg',
            factor=26.93
        ),
        UsageType(
            name='heating',
            unit='l',
            factor=10
        )
    ])


filipe_usage_data = [
    {
        'name': 'water',
        'unit': 'kg',
        'amount': 10,
        'date': datetime(2021, 7, 26, tzinfo=pytz.UTC)
    },
    {
        'name': 'water',
        'unit': 'kg',
        'amount': 5,
        'date': datetime(2021, 4, 25, tzinfo=pytz.UTC)
    },
    {
        'name': 'water',
        'unit': 'kg',
        'amount': 20,
        'date': datetime(2021, 4, 23, tzinfo=pytz.UTC)
    },
    {
        'name': 'heating',
        'unit': 'l',
        'amount': 30,
        'date': datetime(2021, 7, 22, tzinfo=pytz.UTC)
    },
    {
        'name': 'heating',
        'unit': 'l',
        'amount': 40,
        'date': datetime(2020, 4, 25, tzinfo=pytz.UTC)
    },
]


john_usage_data = [
    {
        'name': 'water',
        'unit': 'kg',
        'amount': 102,
        'date': datetime(2021, 2, 1, tzinfo=pytz.UTC)
    },
    {
        'name': 'water',
        'unit': 'kg',
        'amount': 53,
        'date': datetime(2021, 3, 11, tzinfo=pytz.UTC)
    },
    {
        'name': 'water',
        'unit': 'kg',
        'amount': 203,
        'date': datetime(2020, 4, 21, tzinfo=pytz.UTC)
    }
]


def create_usage_for_users():
    user = User.objects.get(email='filipe@example.com')
    create_usage(user, filipe_usage_data)

    user = User.objects.get(email='john@example.com')
    create_usage(user, john_usage_data)


def create_usage(user, usage_data):
    for usage_info in usage_data:
        amount = usage_info['amount']
        usage_type = UsageType.objects.get(
            name=usage_info['name'],
            unit=usage_info['unit']
        )

        Usage.objects.create(
            usage_type=usage_type,
            user=user,
            amount=amount,
            usage_at=usage_info['date'],
            calculated_emissions=get_calculated_emissions(
                amount, usage_type.factor),
        )
