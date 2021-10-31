from django.contrib.auth.models import User


def create_user(username: str, email: str, password: str) -> User:
    user = User(username=username, email=email, is_superuser=False,)
    user.set_password(password)
    user.save()
    return user
