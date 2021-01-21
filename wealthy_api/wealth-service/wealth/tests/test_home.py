import pytest

from django.urls import reverse, resolve
from django.test import RequestFactory
from mixer.backend.django import mixer
from django.contrib.auth.models import User, AnonymousUser
from wealth.wealth.views import home_view


@pytest.fixture
def home_setup(db):
    url = reverse('home')
    view = resolve('/home/')
    request = RequestFactory()
    user = mixer.blend(User)
    setup = {
        'url': url,
        'view': view,
        'request': request,
        'user': user,
    }
    return setup


def test_home_url(home_setup):
    assert resolve(home_setup['url']).view_name == 'home'


def test_home_view_authenticated(home_setup):
    request = home_setup['request'].get(home_setup['url'])
    request.user = home_setup['user']
    response = home_view(request)
    assert response.status_code == 200


def test_home_view_unauthenticated(home_setup):
    request = home_setup['request'].get(home_setup['url'])
    request.user = AnonymousUser()
    response = home_view(request)
    assert 'accounts/login' in response.url


def test_home_url_resolves_view(home_setup):
    assert home_setup['view'].func == home_view

