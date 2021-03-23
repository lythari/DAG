import operator
import time
from http import HTTPStatus
from django.http import HttpResponse
from django.test.client import Client
import pytest

URL = ''


@pytest.fixture(scope='module')
def response():
    return Client().get(URL)


def test_homepage_reachable(response):
    assert response.status_code == HTTPStatus.OK


def test_homepage_template_found(response):
    expected = sorted(['homepage/index.html', 'templates/base.html'])
    templates = sorted(response.templates, key=operator.attrgetter('name'))
    assert ",".join(t.name for t in templates) == ",".join(expected)


def test_homepage_rendering(response):
    assert isinstance(response, HttpResponse)
    assert b'It Works !' in response.content


def test_homepage_speed(client):
    start_time = time.perf_counter()
    _ = client.get(URL)
    end_time = time.perf_counter()
    duration = end_time-start_time
    assert duration < 0.01
