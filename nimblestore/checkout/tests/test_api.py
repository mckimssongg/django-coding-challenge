import os

import django
import pytest

# from checkout.models import Product
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "nimblestore.settings")
django.setup()


@pytest.fixture
def api_client():
    return APIClient()


# TODO change to fit your product properties
@pytest.fixture
def create_product():
    # pass
    from checkout.models import Product
    def _create_product(name, price, quantity):
        return Product.objects.create(name=name, price=price, quantity=quantity)
    return _create_product


def dummy_test():
    assert 1 == 1


def dummy_failing():
    assert 1 == 2

@pytest.mark.django_db
def test_get_products(api_client, create_product):
    create_product(name="Test Product 1", price=10.00, quantity=100)
    create_product(name="Test Product 2", price=15.00, quantity=200)

    url = reverse("product-list")  # Adjust this to your actual URL name
    response = api_client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 2

@pytest.mark.django_db
def test_post_order(api_client, create_product):
    product1 = create_product(name="Test Product 1", price=10.00, quantity=100)
    product2 = create_product(name="Test Product 2", price=15.00, quantity=200)

    order_data = [
        {"product": "Test Product 1", "quantity": 5},
        {"product": "Test Product 2", "quantity": 10},
    ]

    url = reverse("order")
    response = api_client.post(url, order_data, format='json')

    assert response.status_code == status.HTTP_200_OK
    expected_total = (5 * 10.00) + (10 * 15.00)
    assert response.data['total'] == expected_total

    # Verificamos que las cantidades se hayan actualizado
    product1.refresh_from_db()
    product2.refresh_from_db()
    assert product1.quantity == 95
    assert product2.quantity == 190