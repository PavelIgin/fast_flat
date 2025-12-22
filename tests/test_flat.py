from unittest.mock import patch

import pytest
from fastapi.testclient import TestClient


async def mock_send_message_about_created_flat_service(item):
    pass


@patch(
    "flat.service.flat_services.send_message_about_created_flat_service",
    mock_send_message_about_created_flat_service,
)
@pytest.mark.anyio
async def test_create_flat(client: TestClient, auth_user):
    data = {
        "cost": 0,
        # "photos": [
        #     "string"
        # ], # todo додумать как замокать работу с ссылками на файлы
        "user": {"email": "user@example.com", "telegram_contact": "string"},
        "quadrature": 0,
        "floor": 0,
        "address": "string",
        "is_active": True,
    }
    response = client.post(
        url="/flat",
        json=data,
        headers={"Authorization": f"Bearer {auth_user}"},
    )
    assert response.status_code == 200


@pytest.mark.anyio
async def test_retrieve_flat(client: TestClient, auth_user, flat: int):
    response = client.get(
        url=f"/flat/{flat}",
        headers={"Authorization": f"Bearer {auth_user}"},
    )
    assert response.status_code == 200


@pytest.mark.anyio
async def test_list_flat(client: TestClient, auth_user: dict, flat: int):
    response = client.get(
        url="/flat/",
        headers={"Authorization": f"Bearer {auth_user}"},
    )
    assert response.status_code == 200


@pytest.mark.anyio
async def test_private_retrieve_flat(
    client: TestClient, auth_user: dict, flat: int
):
    response = client.get(
        url=f"/flat/private/{flat}",
        headers={"Authorization": f"Bearer {auth_user}"},
    )
    assert response.status_code == 200


@pytest.mark.anyio
async def test_private_list_flat(
    client: TestClient, auth_user: dict, flat: int
):
    response = client.get(
        url=f"/flat/private/",
        headers={"Authorization": f"Bearer {auth_user}"},
    )
    assert response.status_code == 200
