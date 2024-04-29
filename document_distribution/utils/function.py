from django.utils import timezone
import random
from django.shortcuts import redirect
from django.urls import reverse

def generate_activation_code():
    return int("".join([str(random.randint(1, 9)) for _ in range(6)]))


def login_required(redirect_url="/"):
    def decorator(function):
        def wrapper(request, *args, **kwargs):
            if request.user.is_authenticated:
                return function(request, *args, **kwargs)
            else:
                return redirect(redirect_url)  # Redirect to the specified URL if not authenticated
        return wrapper
    return decorator
