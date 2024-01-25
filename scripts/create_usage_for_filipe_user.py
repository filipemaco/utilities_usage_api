from django.contrib.auth import get_user_model

from usages.tests_utils import filipe_usage_data, create_usage

User = get_user_model()


def create_usage_for_filipe_user():
    user = User.objects.get(email='filipe@test.com')
    create_usage(user, filipe_usage_data)
