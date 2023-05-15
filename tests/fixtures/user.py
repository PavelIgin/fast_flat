import pytest


@pytest.fixture()
async def created_user(apply_migrations: None, client):
    """Main fixture of user."""
    data = {'email': 'useaqqaar@example.com', 'password': 'stqring'}
    response = client.post(url='/auth/register/', json=data)
    assert response.status_code == 201
    return data


@pytest.fixture()
async def auth_user(created_user, client):
    """Main fixture of user."""
    response = client.post(url='/auth/jwt/login', json={'email': 'useaaar@example.com', 'password': 'string'})
    print(response)
    return response['access_token']