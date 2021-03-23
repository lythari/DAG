import operator
import time
from http import HTTPStatus

from django.http import HttpResponse
from django.test import TestCase
from django.test import Client


class HomepageUrlTest(TestCase):

    url = ''

    def setUp(self):
        # Every test needs a client.
        self.client = Client()
        self.response = self.client.get(HomepageUrlTest.url)

    def test_homepage_reachable(self):
        self.assertEqual(self.response.status_code, HTTPStatus.OK)

    def test_homepage_template_found(self):
        expected = sorted(['homepage/index.html', 'templates/base.html'])
        templates = sorted(self.response.templates, key=operator.attrgetter('name'))
        self.assertEqual(",".join(t.name for t in templates), ",".join(expected))

    def test_homepage_rendering(self):
        self.assertIsInstance(self.response, HttpResponse)
        self.assertIn(b'It Works !', self.response.content)

    def test_homepage_speed(self):
        start_time = time.perf_counter()
        self.client.get(HomepageUrlTest.url)
        end_time = time.perf_counter()
        duration = end_time-start_time
        self.assertLess(duration, 0.01)
