import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient

from products.models import Product, Category

User = get_user_model()


@pytest.fixture
def user():
    return User.objects.create_user(
        username="testuser",
        email="test@example.com",
        password="pass-12345",
    )

@pytest.fixture
def category():
    return Category.objects.create(
        name="test_category",
        slug="test_category",
    )

@pytest.fixture
def product():
    return Product.objects.create(
        name = "test_product",
        slug="test_product",
        price = 10.22,
        category = category,
        stock = 10
    )

@pytest.fixture
def api_client():
    client = APIClient()
