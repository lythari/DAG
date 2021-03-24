from http import HTTPStatus

from django.http import HttpResponse
from django.test.client import Client
import pytest
from navbar import models as navbar_models

URL = ''


@pytest.fixture(scope='function')
def response_with_nav(db):
    bar = navbar_models.Navbar.objects.create(
        state=True, position='H'
    )
    link = navbar_models.Link.objects.create(
        name="test", position=1, bar=bar
    )
    return Client().get(URL)


@pytest.fixture(scope='function')
def response(db):
    return Client().get(URL)


@pytest.mark.django_db
def test_navbar_saved():
    bar = navbar_models.Navbar.objects.create(
        state=True, position='H'
    )
    h_bar = navbar_models.Navbar.objects.filter(state=True).filter(position='H').first()
    assert bar == h_bar


@pytest.mark.django_db
def test_navbar_context_processor(response):
    assert response.status_code == HTTPStatus.OK


@pytest.mark.django_db
def test_navbar_allow_rendering(response_with_nav):
    assert isinstance(response_with_nav, HttpResponse)
    assert b'<nav id="navigation"' in response_with_nav.content

