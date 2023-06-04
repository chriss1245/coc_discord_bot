"""
Base class for all API connections
"""

import inspect
from abc import ABC, abstractmethod
from dataclasses import field
from enum import Enum
from typing import Any, Dict

import requests
import urllib3


class Method(Enum):
    """
    Enum to store HTTP methods
    """

    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    DELETE = "DELETE"


class NotOkException(Exception):
    """
    Exception raised when the response is not ok
    """

    def __init__(self, method_name: str, response: requests.Response):
        self.response = response
        self.message = (
            f"Response is not ok, status code: {response.status_code}"
            + f"Method: {method_name}\n"
            + f", reason: {response.reason}\n{response.text}"
        )
        super().__init__(self.message)


class BaseClient(ABC):
    """
    Class to handle basic behavior of API connections
    """

    def __init__(
        self,
        token: str = field(default_factory=str),
        headers: Dict[str, str] = field(default_factory=dict),
    ):
        """
        Base Api connection

        Args:
            base_url (str): Base url of the API
            token (str, optional): API token. Defaults to None.
            headers (dict, optional): Headers to be used in the requests. Defaults to None.
            endpoints (dict, optional): Endpoints of the API. Defaults to None.
        """

        self.token = token
        self.headers = headers

    @abstractmethod
    def add_token(self, request: requests.Request) -> requests.Request:
        """
        Add a token to the request.

        Args:
            request (requests.Request): The request to add the token to.

        Returns:
            requests.Request: The request with the token added.
        """
        raise NotImplementedError

    @abstractmethod
    def error_handler(self, response: requests.Response, method_name: str):
        """
        Handle an error response

        Args:
            response (requests.Response): Response to handle
        """
        raise NotImplementedError

    def process_request(self, url: str, method: Method = Method.GET, **kwargs):
        """
        Process a generic request
        Args:
            url (str): Url of the request
            method (Method, optional): HTTP method. Defaults to Method.GET.
            kwargs: Keyword arguments to be passed to the request

        Returns:
            dict: Response json
        """

        clean_url = urllib3.util.parse_url(url).url
        request = requests.Request(
            method.value, clean_url, headers=self.headers, **kwargs
        )
        request = self.add_token(request=request)

        with requests.Session() as session:
            response = session.send(request.prepare())

        if not response.ok:
            # get the name of the method which called this function from the stack
            method_name = inspect.stack()[1].function
            self.error_handler(response=response, method_name=method_name)

        return response.json()
