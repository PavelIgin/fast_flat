import pytest


@pytest.mark.anyio
async def test_create_tenting(client, flat, auth_user):
    data = {
        "lease_range": {"start": "2025-05-26", "end": "2025-05-27"},
        "count_guest": 1,
        "flat_id": str(flat),
    }
    response = client.post(
        url="/renting/",
        json=data,
        headers={"Authorization": f"Bearer {auth_user}"},
    )
    assert (
        response.status_code == 200
    )  # todo понять как делать 201 статус, в доке показывает 201, но в тесте 200


@pytest.mark.anyio
async def test_retrieve_tenting(client, base_renting, auth_user):
    response = client.get(
        url="/renting/private",
        headers={"Authorization": f"Bearer {auth_user}"},
    )
    assert (
        response.status_code == 200
    )  # todo понять как делать 201 статус, в доке показывает 201, но в тесте 200
