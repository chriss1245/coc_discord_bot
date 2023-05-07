"""
Base class for all API connections
"""

from abc import ABC, abstractmethod
from urllib.parse import quote

import inspect
import re
import requests

from discord_clash_bot.utils.logging import get_module_logger

class BaseClient(ABC):
    """
    Class to handle basic behavior of API connections
    """
    logger = get_module_logger(__name__)
    endpoints_dict = {}
    base_url = None
    headers = None
    __instance = None

    def __init__(self, token: str = None):
        """
        Base Api connection

        Args:
            base_url (str): Base url of the API
            token (str, optional): API token. Defaults to None.
            headers (dict, optional): Headers to be used in the requests. Defaults to None.
            endpoints (dict, optional): Endpoints of the API. Defaults to None.
        """
        if self.__instance is not None:
            return

        self.token = token

        for method, endpoint in self.endpoints_dict.items():
            setattr(self, method, self.build_endpoint_handler(method, endpoint))

        self.__instance = self

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

    def process_response(self, response: requests.Response):
        """
        Post process the response
        Args:
            response (requests.Response): Response of the request

        Returns:
            dict: Response json

        Raises:
            requests.HTTPError: If the response is not ok
        """
        self.logger.debug(f"Response: {response.status_code} {response.reason}, {response.text}")
        if not response.ok:
            # get the name of the method which called this function from the stack
            method_name = inspect.stack()[1].function

            response_json = response.json()
            error_msg = (f"Error {response.status_code}: {response_json['reason']}\n" +
                        f"Method: {method_name}\n" + 
                        f"{response_json['message']}")
            raise requests.HTTPError(error_msg)

        return response.json()

    def build_endpoint_handler(self, name: str, endpoint: str ) -> callable:
        """
        Builds a handler for a specific endpoint dynamically when the class is instantiated.

        Args:
            name (str): Name of the handler
            endpoint (str): Endpoint of the handlers

        Returns:
            callable: A function that handles the endpoint
        """

        arg_names = re.findall(r"\{(\w+)\}", endpoint)

        self.logger.debug(f"Building handler for {name} with args: {arg_names}")

        def handler(*args, data=None, json=None, query_params=None) -> dict or list:
            """
            Handler for the endpoint: {endpoint}

            Args:
                {arg_names}: Arguments of the endpoint
                data (dict, optional): Data to be sent in the request.
                    Encoded as form data. Defaults to None.
                json (dict, optional): Json to be sent in the request. Defaults to None.
                query_params (dict, optional): Query parameters to be sent in the request. 
            """

            # handle special characters in the arguments
            for arg in args:
                if isinstance(arg, str):
                    arg = quote(arg)

            endpoint_args = dict(zip(arg_names, args))
            final_endpoint = endpoint.format(**endpoint_args)

            # get the request type from the name of the method (e.g. get_clan -> GET)
            request_type = name.split("_")[0].upper()
            request = requests.Request(request_type, self.base_url + final_endpoint,
                                        headers=self.headers, data=data, json=json)
            request = self.add_token(request)
            if query_params:
                request.params = query_params
            prepared_request = request.prepare()
            self.logger.debug(f"Request: {prepared_request.method} {prepared_request.url}")

            with requests.Session() as session:
                response = session.send(prepared_request)
            
            return self.process_response(response)

        handler.__name__ = name
        return handler
