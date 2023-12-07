import pytest
from django.urls import reverse
from django.contrib.auth.models import User
from django.test import Client

@pytest.fixture
def client():
    return Client()

@pytest.fixture
def user(django_user_model):
    user = django_user_model.objects.create_user(username='user', password='password')
    return user

# Test for the index view
def test_index_view(client):
    url = reverse('index')
    response = client.get(url)
    assert response.status_code == 200
    assert 'monapp/index.html' in [t.name for t in response.templates]

# Test the GET request for the login view
def test_login_view_get(client):
    url = reverse('login')
    response = client.get(url)
    assert response.status_code == 200
    assert 'monapp/login.html' in [t.name for t in response.templates]

# Test a valid POST request for the login view
@pytest.mark.django_db
def test_login_view_post_valid(client, user):
    url = reverse('login')
    response = client.post(url, {'username': 'user', 'password': 'password'})
    assert response.status_code == 302
    assert response.url == reverse('welcome')

# Test an invalid POST request for the login view
@pytest.mark.django_db
def test_login_view_post_invalid(client, user):
    url = reverse('login')
    response = client.post(url, {'username': 'user', 'password': 'wrongpassword'})
    assert response.status_code == 200
    assert 'form' in response.context
    assert not response.context['form'].is_valid()
    assert response.context['form'].errors

# Test the welcome view with authenticated user
@pytest.mark.django_db
def test_welcome_view_authenticated(client, user):
    client.force_login(user)
    url = reverse('welcome')
    response = client.get(url)
    assert response.status_code == 200
    assert 'monapp/welcome.html' in [t.name for t in response.templates]

# Test the welcome view with unauthenticated access
def test_welcome_view_unauthenticated(client):
    url = reverse('welcome')
    response = client.get(url)
    assert response.status_code == 302
    assert response.url.startswith('/accounts/login/')

# Test the logout view
@pytest.mark.django_db
def test_logout_view(client, user):
    client.force_login(user)
    url = reverse('logout')
    response = client.get(url)
    assert response.status_code == 302
    assert response.url == reverse('index')
    assert '_auth_user_id' not in client.session
