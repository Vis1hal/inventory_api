from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from .models import Product

class ProductStockTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.product = Product.objects.create(name="Test Product", stock_quantity=10)

    def test_add_stock(self):
        response = self.client.post(f'/api/products/{self.product.id}/add_stock/', {'quantity': 5})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.product.refresh_from_db()
        self.assertEqual(self.product.stock_quantity, 15)

    def test_add_stock_invalid_quantity(self):
        response = self.client.post(f'/api/products/{self.product.id}/add_stock/', {'quantity': -1})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_remove_stock(self):
        response = self.client.post(f'/api/products/{self.product.id}/remove_stock/', {'quantity': 3})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.product.refresh_from_db()
        self.assertEqual(self.product.stock_quantity, 7)

    def test_remove_stock_insufficient(self):
        response = self.client.post(f'/api/products/{self.product.id}/remove_stock/', {'quantity': 15})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.product.refresh_from_db()
        self.assertEqual(self.product.stock_quantity, 10) 

    def test_remove_stock_zero_quantity(self):
        response = self.client.post(f'/api/products/{self.product.id}/remove_stock/', {'quantity': 0})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_negative_stock(self):
        response = self.client.patch(f'/api/products/{self.product.id}/', {'stock_quantity': -5})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_low_stock_list(self):
        Product.objects.create(name="Low Stock", stock_quantity=5, low_stock_threshold=10)
        Product.objects.create(name="Normal Stock", stock_quantity=15, low_stock_threshold=10)
        response = self.client.get('/api/products/low_stock/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)  