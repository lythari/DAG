from http import HTTPStatus

from django.http import HttpResponse
from django.test.client import Client
import pytest
from navbar import models as navbar_models

URL = ''


@pytest.fixture(scope='function')
def response_with_nav(db):
    def gen_response(style):
        _ = navbar_models.Navbar.objects.create(
            state=True, position='H', style=style
        )
        return Client().get(URL)
    return gen_response


@pytest.mark.django_db
@pytest.mark.parametrize("position", ['H', 'VL', 'VC'])
def test_navbar_style_noreg(position):
    bar = navbar_models.Navbar.objects.create(
        state=True, position=position, style=1
    )
    assert bar.position == position


@pytest.mark.django_db
@pytest.mark.parametrize("style,classe", list(navbar_models.Navbar.STYLE_CHOICES))
def test_navbar_style_renders(response_with_nav, style, classe):
    response = response_with_nav(style)
    assert isinstance(response, HttpResponse)
    assert b'<nav id="navigation"' in response.content
    assert bytes(classe, 'ASCII') in response.content
