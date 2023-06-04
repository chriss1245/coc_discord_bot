import unittest
from unittest.mock import Mock, patch
from discord_clash_bot.api.base_client import BaseClient, Method
import requests


class MockClient(BaseClient):
    """Mock client for testing"""

    def add_token(self, request: requests.Request) -> requests.Request:
        request.headers["Authorization"] = f"Bearer {self.token}"
        return request

    def error_handler(self, response: requests.Response, method_name: str):
        raise NotImplementedError


class TestBaseClient(unittest.TestCase):
    """Test the BaseClient class"""

    def setUp(self):
        self.client = MockClient(
            token="test-token", headers={"Content-Type": "application/json"}
        )

    @patch("requests.Session.send")
    def test_process_request_success(self, mock_get):
        """
        Test whether the process_request method returns the correct response
        """

        mock_response = Mock()
        mock_response.ok = True
        mock_response.json.return_value = {"status": "ok"}
        mock_get.return_value = mock_response

        response = self.client.process_request("https://nothig.com", method=Method.GET)
        self.assertEqual(response, mock_response.json())

    @patch("requests.Session.send")
    def test_process_request_not_ok(self, mock_get):
        """
        Test whether the process_request method raises a NotOkException
        """

        mock_response = Mock()
        mock_response.ok = False
        mock_response.json.return_value = {"status": "ok"}
        mock_get.return_value = mock_response

        with self.assertRaises(NotImplementedError):
            self.client.process_request("https://nothig.com", method=Method.GET)
