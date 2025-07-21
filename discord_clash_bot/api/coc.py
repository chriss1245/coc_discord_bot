"""
Clash of Clans API wrapper
"""

from typing import Any, Dict, List

import requests
from discord_clash_bot.utils.logging import get_logger

from .base_client import BaseClient, Method, NotOkException

logger = get_logger(__name__)


class PlayerNotFound(Exception):
    """
    Raised when the user tag format is invalid
    """

    def __init__(self):
        super().__init__("Invalid user tag")


class ClanNotFound(Exception):
    """
    Raised when the clan tag format is invalid or the clan does not exist
    """

    def __init__(self):
        super().__init__("Invalid clan tag")


class ServerException(Exception):
    """
    Raised when the server returns an error of the type 5xx
    """

    def __init__(self, response: requests.Response):
        self.response = response
        super().__init__(
            f"Server error: {response.status_code} {response.reason}\n{response.text}"
        )


class CocClient(BaseClient):
    """
    Clash of Clans API wrapper
    """

    base_url = "https://api.clashofclans.com/v1/"

    endpoints_dict = {
        "get_clan": "clans/{clan_tag}",
        "get_war": "clans/{clan_tag}/currentwar",
        "get_player": "players/{player_tag}",
        "get_clan_members": "clans/{clan_tag}/members",
        "get_capital_raidseasons": "clans/{clan_tag}/capitalraidseasons",
        "post_verify_player": "players/{player_tag}/verifytoken",
    }

    def add_token(self, request: requests.Request) -> requests.Request:
        """
        Add a token to the request.

        Args:
            request (requests.Request): The request to add the token to.

        Returns:
            requests.Request: The request with the token added.
        """
        request.headers["Authorization"] = f"Bearer {self.token}"
        return request

    def error_handler(self, response: requests.Response, method_name: str):
        """
        Handle an error response

        Args:
            response (requests.Response): Response to handle
        """
        if response.status_code == 404:
            if method_name == "get_player":
                raise PlayerNotFound()
            if method_name in ["get_clan", "get_war", "get_clan_members"]:
                raise ClanNotFound()
        elif response.status_code >= 500:
            raise ServerException(response)
        else:
            raise NotOkException(response=response, method_name=method_name)

    def get_clan(self, clan_tag) -> List[Dict[str, Any]]:
        """
        Returns clan information

        Args:
            clan_tag (str): Tag of the clan

        Returns:
            dict: Clan information
        """

        url_raw = self.base_url + self.endpoints_dict["get_clan"].format(
            clan_tag=clan_tag
        )

        return self.process_request(url_raw, method=Method.GET)["body"]

    def get_war(self, clan_tag) -> Dict[str, Any]:
        """
        Returns current war information

        Args:
            clan_tag (str): Tag of the clan

        Returns:
            dict: War information
        """

        url_raw = self.base_url + self.endpoints_dict["get_war"].format(
            clan_tag=clan_tag
        )

        return self.process_request(url_raw, method=Method.GET)["body"]

    def get_player(self, player_tag) -> Dict[str, Any]:
        """
        Returns player information

        Args:
            player_tag (str): Tag of the player

        Returns:
            dict: Player information
        """

        url_raw = self.base_url + self.endpoints_dict["get_player"].format(
            player_tag=player_tag
        )

        return self.process_request(url_raw, method=Method.GET)["body"]

    def get_clan_members(self, clan_tag) -> Dict[str, Any]:
        """
        Returns clan members information

        Args:
            clan_tag (str): Tag of the clan

        Returns:
            dict: Clan members information
        """

        url_raw = self.base_url + self.endpoints_dict["get_clan_members"].format(
            clan_tag=clan_tag
        )

        return self.process_request(url_raw, method=Method.GET)["body"]

    def get_capital_raidseasons(self, clan_tag) -> Dict[str, Any]:
        """
        Returns capital raid seasons information

        Args:
            clan_tag (str): Tag of the clan

        Returns:
            dict: Capital raid seasons information
        """

        url_raw = self.base_url + self.endpoints_dict["get_capital_raidseasons"].format(
            clan_tag=clan_tag
        )

        return self.process_request(url_raw, method=Method.GET)["body"]

    def post_verify_player(self, player_tag, token) -> bool:
        """
        Verify player token

        Args:
            player_tag (str): Tag of the player
            token (str): Token to verify

        Returns:
            dict: Verify token response
        """

        url_raw = self.base_url + self.endpoints_dict["post_verify_player"].format(
            player_tag=player_tag
        )

        result = self.process_request(
            url_raw, method=Method.POST, json={"token": token}
        )

        return result["body"]["status"] == "ok"
