from django.contrib.auth import get_user_model

UserModel = get_user_model()


def create_users():
    users = [
        ['filipe@test.com', 'Filipe Santos', 'Password'],
        ['jose@test.com', 'Jose Figueira', 'Password'],
        ['miguel@test.com', 'Miguel Santos', 'Password'],
    ]

    for user in users:
        UserModel.objects.create_user(
            email=user[0],
            name=user[1],
            password=user[2]
        )
