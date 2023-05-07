"""
Clash of Clans API wrapper
"""

import requests

from .base import BaseClient

class CocClient(BaseClient):
    """
    Clash of Clans API wrapper
    """
    endpoints_dict = {
        "get_clan": "clans/{clan_tag}",
        "get_war": "clans/{clan_tag}/currentwar",
        "get_player": "players/{player_tag}",
        "get_clan_members": "clans/{clan_tag}/members",
        "get_capital_raidseasons": "clans/{clan_tag}/capitalraidseasons",
        "post_verify_player": "players/{player_tag}/verifytoken"
    }

    def add_token(self, request: requests.Request) -> requests.Request:
        """
        Add a token to the request.
        """
        request.headers["Authorization"] = f"Bearer {self.token}"
        return request
