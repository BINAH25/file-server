from django.utils import timezone
import random

def generate_activation_code():
    return int("".join([str(random.randint(1, 9)) for _ in range(6)]))

def get_all_user_permissions(user):
    permissions = []
    for perm in user.get_all_permissions():
        permissions.append(perm.split(".")[-1])
    return sorted(permissions)
