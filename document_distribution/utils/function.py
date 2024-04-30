from django.utils import timezone
import random

def generate_activation_code():
    return int("".join([str(random.randint(1, 9)) for _ in range(6)]))

