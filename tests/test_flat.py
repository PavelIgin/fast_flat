# import pytest
# from fastapi.testclient import TestClient
#
#
# @pytest.mark.anyio
# async def test_create_flat(client: TestClient, created_user):
#     data = {
#         "cost": 0,
#         "photos": [
#             "string"
#         ],
#         "user": {
#             "email": "user@example.com",
#             "telegram_contact": "string"
#         },
#         "quadrature": 0,
#         "floor": 0,
#         "address": "string",
#         "is_active": True
#     }
#     response = client.post(url='/flat', json=data)
#     assert response.status_code == 200
#
#
