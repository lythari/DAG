from http import HTTPStatus

from django.http import HttpResponse
from django.test.client import Client
import pytest
from navbar import models as navbar_models

URL = ''


@pytest.fixture(scope='function')
def simple_response(db):
    bar = navbar_models.Navbar.objects.create(
        state=True, position='H'
    )
    _ = navbar_models.Link.objects.create(
        name="test", position=1, bar=bar
    )
    return Client().get(URL)


@pytest.fixture(scope='function')
def response_with_nav(db):
    def get_response(position, has_link=True):
        bar = navbar_models.Navbar.objects.create(
            state=True, position=position
        )
        if has_link:
            _ = navbar_models.Link.objects.create(
                name="test", slug="test", position=1, bar=bar
            )
        return Client().get(URL)
    return get_response


@pytest.fixture(scope='function')
def response(db):
    return Client().get(URL)


@pytest.mark.django_db
def test_navbar_saved():
    bar = navbar_models.Navbar.objects.create(
        state=True, position='H'
    )
    h_bar = navbar_models.Navbar.objects.filter(state=True).first()
    assert bar == h_bar


@pytest.mark.django_db
@pytest.mark.parametrize("position, position_name", navbar_models.Navbar.POSITION_CHOICES)
def test_navbar_position(position, position_name):
    bar = navbar_models.Navbar.objects.create(
        state=True, position=position
    )
    assert bar.position == position
    assert bar.get_position_display() == position_name


@pytest.mark.django_db
def test_navbar_context_processor(response):
    assert response.status_code == HTTPStatus.OK


@pytest.mark.django_db
def test_navbar_renders(simple_response):
    assert isinstance(simple_response, HttpResponse)
    assert b'<nav id="navigation"' in simple_response.content


@pytest.mark.django_db
@pytest.mark.parametrize("position, position_name", navbar_models.Navbar.POSITION_CHOICES)
def test_navbar_render_depend_on_position(response_with_nav, position, position_name):
    response = response_with_nav(position)
    expected_templates = [
        'navbar/link.html',
        navbar_models.Navbar.template_name.get(position_name),
    ]
    templates = [t.name for t in response.templates]
    assert all(a in templates for a in expected_templates)
