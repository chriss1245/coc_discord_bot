"""
Testing cases for coc_client.py
"""

import unittest
from unittest.mock import Mock, patch

import requests
from discord_clash_bot.api.base_client import NotOkException
from discord_clash_bot.api.coc import (
    CocClient,
    ServerException,
    PlayerNotFound,
    ClanNotFound,
)

TOKEN = "test-token"


class TestCocClient(unittest.TestCase):
    """
    Unit tests for CocClient
    """

    def setUp(self):
        self.client_token = TOKEN
        self.client = CocClient(
            token=self.client_token, headers={"Content-Type": "application/json"}
        )

    def test_add_token(self):
        """
        Test whether the barer token is added to the request
        """

        request = requests.Request("GET", "https://nothig.com")
        request = self.client.add_token(request)
        self.assertEqual(
            request.headers["Authorization"], f"Bearer {self.client.token}"
        )

    @patch("requests.Session.send")
    def test_get_clan_success(self, mock_get):
        """
        Test whether the get_clan method returns the correct response
        """

        mock_response = Mock()
        mock_response.ok = True
        mock_response.json.return_value = {
            "body": {"clan": "test-clan", "opponent": "test-opponent"}
        }
        mock_get.return_value = mock_response

        result = self.client.get_clan("test-clan")
        self.assertEqual(result, mock_response.json()["body"])

    @patch("requests.Session.send")
    def test_get_clan_not_ok(self, mock_get):
        """
        Test whether the get_clan method raises an exception when the response is not ok
        """

        mock_response = Mock()
        mock_response.ok = False
        mock_response.status_code = 404
        mock_response.json.return_value = {"status": "not ok"}
        mock_get.return_value = mock_response

        with self.assertRaises(ClanNotFound):
            self.client.get_clan("test-clan")

    @patch("requests.Session.send")
    def test_get_clan_members_success(self, mock_get):
        """
        Test whether the get_clan_members method returns the correct response
        """

        mock_response = Mock()
        mock_response.ok = True
        mock_response.json.return_value = {
            "body": [{"name": "test-name", "tag": "test-tag"}]
        }
        mock_get.return_value = mock_response

        result = self.client.get_clan_members("test-clan")
        self.assertEqual(result, mock_response.json()["body"])

    @patch("requests.Session.send")
    def test_get_clan_members_not_ok(self, mock_get):
        """Test whether the get_clan_members method raises an exception when the response is not ok"""

        mock_response = Mock()
        mock_response.ok = False
        mock_response.json.return_value = {"status": "not ok"}
        mock_response.status_code = 404
        mock_get.return_value = mock_response

        with self.assertRaises(ClanNotFound):
            self.client.get_clan_members("test-clan")

    @patch("requests.Session.send")
    def test_get_war_success(self, mock_get):
        """
        Test whether the get_war method returns the correct response
        """

        mock_response = Mock()
        mock_response.ok = True
        mock_response.json.return_value = {
            "body": {"clan": "test-clan", "opponent": "test-opponent"}
        }
        mock_get.return_value = mock_response

        result = self.client.get_war("test-clan")
        self.assertEqual(result, mock_response.json()["body"])

    @patch("requests.Session.send")
    def test_get_war_not_ok(self, mock_get):
        """
        Test whether the get_war method raises an exception when the response is not ok
        """

        mock_response = Mock()
        mock_response.ok = False
        mock_response.status_code = 404
        mock_response.json.return_value = {"status": "not ok"}
        mock_get.return_value = mock_response

        with self.assertRaises(ClanNotFound):
            self.client.get_war("test-clan")

    @patch("requests.Session.send")
    def test_get_player(self, mock_get):
        """
        Test whether the get_player method returns the correct response
        """

        mock_response = Mock()
        mock_response.ok = True
        mock_response.json.return_value = {"body": {"status": "ok"}}
        mock_get.return_value = mock_response

        result = self.client.get_player("test-player")
        self.assertEqual(result, mock_response.json()["body"])

    @patch("requests.Session.send")
    def test_get_player_not_found(self, mock_get):
        """
        Test whether the get_player method raises an exception when the response is not ok
        """

        mock_response = Mock()
        mock_response.ok = False
        mock_response.status_code = 404
        mock_response.json.return_value = {"status": "not ok"}
        mock_get.return_value = mock_response

        with self.assertRaises(PlayerNotFound):
            self.client.get_player("test-player")

    @patch("requests.Session.send")
    def test_get_player_server_error(self, mock_get):
        """
        Test whether the get_player method raises an exception when the response is not ok
        """

        mock_response = Mock()
        mock_response.ok = False
        mock_response.status_code = 500
        mock_response.json.return_value = {"status": "not ok"}
        mock_get.return_value = mock_response

        with self.assertRaises(ServerException):
            self.client.get_player("test-player")

    @patch("requests.Session.send")
    def test_not_ok(self, mock_get):
        """
        Test whether the get_player method raises an exception when the response is not ok
        """

        mock_response = Mock()
        mock_response.ok = False
        mock_response.status_code = 454
        mock_response.json.return_value = {"status": "not ok"}
        mock_get.return_value = mock_response

        with self.assertRaises(NotOkException):
            self.client.get_player("test-player")

    @patch("requests.Session.send")
    def test_post_verify_player(self, mock_post):
        """
        Test whether the post_verify_player method returns the correct response
        """

        mock_response = Mock()
        mock_response.ok = True
        # use mock_verify_player to mock the response
        mock_post.side_effect = mock_verify_player

        result = self.client.post_verify_player("player", "test-token")
        self.assertTrue(result)

    @patch("requests.Session.send")
    def test_post_verify_player_not_ok(self, mock_post):
        """
        Test whether the post_verify_player method returns the correct response
        """

        mock_response = Mock()
        mock_response.ok = True
        # use mock_verify_player to mock the response
        mock_post.side_effect = mock_verify_player

        result = self.client.post_verify_player("player", "wrong-token")
        self.assertFalse(result)


def mock_verify_player(request: requests.PreparedRequest):
    """
    Mock verify player. It accepts a token in the request body
    """

    if request.body == b'{"token": "test-token"}':
        response = Mock()
        response.ok = True
        response.json.return_value = {"body": {"status": "ok"}}
        return response

    response = Mock()
    response.ok = True
    response.json.return_value = {"body": {"status": "invalid"}}
    return response
