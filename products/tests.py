
from decimal import Decimal

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Product


class ProductAPITests(APITestCase):

    def setUp(self):
        # Create a product used by the tests.
        self.product = Product.objects.create(
            name="Wireless Mouse",
            description="Bluetooth mouse",
            price=Decimal("599.99"),
            stock_quantity=25,
            category="Electronics",
        )

        self.list_url = reverse("product-list")
        self.detail_url = reverse(
            "product-detail",
            args=[self.product.id],
        )

        self.valid_data = {
            "name": "Mechanical Keyboard",
            "description": "RGB gaming keyboard",
            "price": "1499.99",
            "stock_quantity": 10,
            "category": "Electronics",
        }

    def test_create_product(self):
        response = self.client.post(
            self.list_url,
            self.valid_data,
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
        )
        self.assertEqual(Product.objects.count(), 2)
        self.assertEqual(
            response.data["name"],
            "Mechanical Keyboard",
        )

    def test_fetch_product_list(self):
        response = self.client.get(self.list_url)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )
        self.assertEqual(len(response.data), 1)
        self.assertEqual(
            response.data[0]["name"],
            "Wireless Mouse",
        )

    def test_fetch_product_details(self):
        response = self.client.get(self.detail_url)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )
        self.assertEqual(
            response.data["name"],
            "Wireless Mouse",
        )
        self.assertEqual(
            response.data["price"],
            "599.99",
        )

    def test_update_product(self):
        updated_data = {
            "name": "Wireless Mouse Pro",
            "description": "Updated Bluetooth mouse",
            "price": "799.99",
            "stock_quantity": 30,
            "category": "Electronics",
        }

        response = self.client.put(
            self.detail_url,
            updated_data,
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.product.refresh_from_db()
        self.assertEqual(
            self.product.name,
            "Wireless Mouse Pro",
        )
        self.assertEqual(
            self.product.price,
            Decimal("799.99"),
        )

    def test_delete_product(self):
        response = self.client.delete(self.detail_url)

        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT,
        )
        self.assertFalse(
            Product.objects.filter(
                id=self.product.id
            ).exists()
        )

    def test_negative_price_is_rejected(self):
        invalid_data = self.valid_data.copy()
        invalid_data["price"] = "-100.00"

        response = self.client.post(
            self.list_url,
            invalid_data,
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )
        self.assertIn("price", response.data)
        self.assertEqual(Product.objects.count(), 1)

    def test_zero_price_is_rejected(self):
        invalid_data = self.valid_data.copy()
        invalid_data["price"] = "0.00"

        response = self.client.post(
            self.list_url,
            invalid_data,
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )
        self.assertIn("price", response.data)

    def test_negative_stock_is_rejected(self):
        invalid_data = self.valid_data.copy()
        invalid_data["stock_quantity"] = -5

        response = self.client.post(
            self.list_url,
            invalid_data,
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )
        self.assertIn("stock_quantity", response.data)
        self.assertEqual(Product.objects.count(), 1)

    def test_nonexistent_product_returns_404(self):
        response = self.client.get(
            reverse("product-detail", args=[99999])
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_404_NOT_FOUND,
        )