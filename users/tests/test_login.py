import re
import unittest

from django.test import Client
from django.urls import reverse

from users.urls.users_urls import urlpatterns as users_urlpatterns
from users.urls.home_urls import urlpatterns as home_urlpatterns


class TestLogins(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.client = Client()

    def test_login(self):
        for prefix, urlpatterns in [('users:', users_urlpatterns), ('home:', home_urlpatterns)]:

            for url in urlpatterns:
                full_url_name = prefix+url.name
                kwargs = {}
                for match in re.finditer(r'<int:(.*?)>', str(url.pattern)):
                    kwargs[match.group(1)] = 1

                try:
                    response = self.client.get(reverse(full_url_name, kwargs=kwargs))
                except:
                    raise Exception(f'{full_url_name} accessible without login!')

                self.assertEqual(response.status_code, 302, msg=f'{full_url_name} accessible without login!')
                self.assertTrue(response.url.startswith('/accounts/login/'), msg=f'{full_url_name} accessible without login!')


if __name__ == '__main__':
    unittest.main()
