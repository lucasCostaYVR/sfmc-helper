# rest_client.py
from sfmc_helper.auth.base_client import BaseClient
from sfmc_helper.utils.exceptions import APIRequestError
from sfmc_helper.utils.logger import logger
import requests

class RestClient(BaseClient):
    """
    A client for interacting with the SFMC REST API.
    """
    def __init__(self, client_id, client_secret, auth_base_url, rest_base_url):
        super().__init__(client_id, client_secret, auth_base_url)
        self.rest_base_url = rest_base_url.rstrip('/')

    def get(self, endpoint, params=None):
        url = f"{self.rest_base_url}/{endpoint.lstrip('/')}"
        headers = {
            'Authorization': f'Bearer {self.get_access_token()}',
            'Content-Type': 'application/json'
        }
        try:
            response = requests.get(url, headers=headers, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"HTTP GET error occurred: {e}")
            raise APIRequestError(f"HTTP GET error occurred: {e}")

    def post(self, endpoint, data=None):
        url = f"{self.rest_base_url}/{endpoint.lstrip('/')}"
        headers = {
            'Authorization': f'Bearer {self.get_access_token()}',
            'Content-Type': 'application/json'
        }
        try:
            response = requests.post(url, headers=headers, json=data)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"HTTP POST error occurred: {e}")
            raise APIRequestError(f"HTTP POST error occurred: {e}")

    # Additional methods (put, delete) can be implemented similarly
