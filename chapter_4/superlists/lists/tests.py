
from django.test import TestCase


# Create your tests here.
class SmokeTest(TestCase):

    def test_uses_home_template(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'home.html')

