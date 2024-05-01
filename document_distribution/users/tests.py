from django.test import Client, TestCase, RequestFactory
from . import views
from users.models import *
from django.urls import reverse

# Create your tests here.

class RegisterTestCase(TestCase):
    def setUp(self):
        # Setting up the RequestFactory to create mock requests
        self.factory = RequestFactory()
        # Creating Code User
        email_address = 'louis@gmail.com'
        code = '123456'
        password = '1234'
        code_user = CodeEmail.objects.create(email_address=email_address,code=code,password=password)
        code_user.save()

    def test_get_register_page(self):
        # Creating a mock GET request to the register page
        request = self.factory.get(reverse('users:register'))  # Use the name of the URL pattern
        # Using the Register view to handle the request
        response = views.Register.as_view()(request)
        # Asserting that the response status code is 200 (OK)
        self.assertEqual(response.status_code, 200)

      