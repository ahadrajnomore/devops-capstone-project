"""
Tests for Customer Accounts Microservice
"""

import unittest
from service import app, reset_data


class TestAccountService(unittest.TestCase):
    """Account service test cases"""

    def setUp(self):
        """Runs before each test"""
        reset_data()
        self.client = app.test_client()

    def create_test_account(self):
        """Helper method to create an account"""
        account_data = {
            "name": "John Doe",
            "email": "john@example.com",
            "address": "123 Main St",
            "phone_number": "555-1212"
        }
        return self.client.post("/accounts", json=account_data)

    def test_index(self):
        """Test root endpoint"""
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data["name"], "Customer Accounts Microservice")

    def test_create_account(self):
        """Test creating an account"""
        response = self.create_test_account()
        self.assertEqual(response.status_code, 201)
        data = response.get_json()
        self.assertEqual(data["name"], "John Doe")
        self.assertEqual(data["email"], "john@example.com")
        self.assertEqual(data["address"], "123 Main St")
        self.assertEqual(data["phone_number"], "555-1212")
        self.assertEqual(data["id"], 1)

    def test_create_account_with_no_data(self):
        """Test creating an account with no JSON data"""
        response = self.client.post("/accounts")
        self.assertEqual(response.status_code, 415)

    def test_create_account_missing_field(self):
        """Test creating an account with missing field"""
        response = self.client.post("/accounts", json={
            "name": "John Doe",
            "email": "john@example.com",
            "address": "123 Main St"
        })
        self.assertEqual(response.status_code, 400)

    def test_list_accounts(self):
        """Test listing accounts"""
        self.create_test_account()
        response = self.client.get("/accounts")
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["name"], "John Doe")

    def test_read_account(self):
        """Test reading an account"""
        self.create_test_account()
        response = self.client.get("/accounts/1")
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data["name"], "John Doe")

    def test_read_account_not_found(self):
        """Test reading an account that does not exist"""
        response = self.client.get("/accounts/999")
        self.assertEqual(response.status_code, 404)

    def test_update_account(self):
        """Test updating an account"""
        self.create_test_account()
        response = self.client.put("/accounts/1", json={
            "name": "John Updated",
            "email": "john.updated@example.com",
            "address": "456 Main St",
            "phone_number": "555-3434"
        })
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data["name"], "John Updated")
        self.assertEqual(data["email"], "john.updated@example.com")

    def test_update_account_not_found(self):
        """Test updating an account that does not exist"""
        response = self.client.put("/accounts/999", json={
            "name": "John Updated"
        })
        self.assertEqual(response.status_code, 404)

    def test_update_account_with_no_data(self):
        """Test updating an account with no JSON data"""
        self.create_test_account()
        response = self.client.put("/accounts/1")
        self.assertEqual(response.status_code, 415)

    def test_delete_account(self):
        """Test deleting an account"""
        self.create_test_account()
        response = self.client.delete("/accounts/1")
        self.assertEqual(response.status_code, 204)

        response = self.client.get("/accounts/1")
        self.assertEqual(response.status_code, 404)

    def test_delete_account_not_found(self):
        """Test deleting an account that does not exist"""
        response = self.client.delete("/accounts/999")
        self.assertEqual(response.status_code, 404)


if __name__ == "__main__":
    unittest.main()
