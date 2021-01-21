import pytest

from django.contrib.auth.models import User
from django.urls import reverse
from django.test import RequestFactory, Client

from wealth.wealth.views import signup


@pytest.fixture
def user_data(db):
    data = {
        'username': 'raf',
        'password1': 'abcd123abcd',
        'password2': 'abcd123abcd',
    }
    return data


@pytest.fixture
def signup_get():
    url = reverse('signup')
    factory = RequestFactory()
    request = factory.get(url)
    response = signup(request)
    return response


@pytest.fixture
def create_user(user_data):
    c = Client()
    url = reverse('signup')
    c.post(url, user_data)


@pytest.fixture
def login_user(create_user):
    url = reverse('login')
    c = Client()
    c.post(url, {'username': 'raf', 'password': 'abcd123abcd'})
    url = reverse('home')
    res = c.get(url)
    user = res.context.get('user')
    return user


def test_signup_status_ok(signup_get):
    """test status code on signup endopint"""
    assert signup_get.status_code == 200


def test_csrf(signup_get):
    """test csrf token in body message"""
    assert 'csrfmiddlewaretoken' in str(signup_get.content)


def test_signup_form(signup_get):
    """test response form"""
    assert '<input' in str(signup_get.content)
    assert 'type="text"' in str(signup_get.content)
    assert 'type="password"' in str(signup_get.content)


def test_full_signup(create_user):
    assert User.objects.exists()


def test_user_authentication(login_user):
    assert login_user.is_authenticated
