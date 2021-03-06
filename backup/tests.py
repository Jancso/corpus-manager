import re
import unittest

from django.test import Client
from django.urls import reverse, URLResolver

from backup.urls import urlpatterns


class TestLogins(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.client = Client()

    def test_login(self):
        for url in urlpatterns:
            if isinstance(url, URLResolver):
                for sub_url in url.url_patterns:
                    self.check(sub_url)
            else:
                self.check(url)

    def check(self, url):
        full_url_name = 'backup:' + url.name
        kwargs = {}
        for match in re.finditer(r'<int:(.*?)>', str(url.pattern)):
            kwargs[match.group(1)] = 1
        try:
            response = self.client.get(reverse(full_url_name, kwargs=kwargs))
        except:
            raise Exception(f'{full_url_name} accessible without login!')

        self.assertEqual(response.status_code, 302,
                         msg=f'Response code is {response.status_code}, '
                             f'{full_url_name} accessible without login!')
        self.assertTrue(
            (response.url.startswith('/accounts/login/')
             or response.url.startswith('/admin/login/')),
            msg=f'Redirect to {response.url}, '
                f'{full_url_name} accessible without login!')


if __name__ == '__main__':
    unittest.main()

