import pytest
from orders.models import Order

@pytest.mark.django_db
def test_orders_require_auth(api_client):
    assert api_client.get('/api/orders/').status_code == 401

