# base_client.py
import requests
import time
import logging

# Configure logging
logger = logging.getLogger(__name__)

class BaseClient:
    """
    A base class for authentication for the SFMC API.
    """
    def __init__(self, client_id, client_secret, auth_base_url):
        self.client_id = client_id
        self.client_secret = client_secret
        self.auth_base_url = auth_base_url.rstrip('/')
        self.access_token = None
        self.token_expiry = None  # Unix timestamp when the token expires
        self.authenticate()

    def authenticate(self):
        """
        Authenticate with the SFMC API and obtain an access token.
        """
        url = f'{self.auth_base_url}/v2/token'
        payload = {
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'grant_type': 'client_credentials'
        }

        try:
            response = requests.post(url, data=payload)
            response.raise_for_status()
            data = response.json()
            self.access_token = data['access_token']
            # Subtract 60 seconds to refresh the token before it actually expires
            self.token_expiry = time.time() + data['expires_in'] - 60
            logger.info("Successfully authenticated and obtained access token.")
        except requests.exceptions.RequestException as e:
            logger.error(f"Authentication failed: {e}")
            raise

    def is_token_expired(self):
        """
        Check if the token is expired or about to expire.

        Returns:
            bool: True if the token is expired, False otherwise.
        """
        return self.token_expiry is None or time.time() >= self.token_expiry

    def get_access_token(self):
        """
        Retrieves a valid access token, refreshing it if necessary.

        Returns:
            str: The valid access token.
        """
        if self.is_token_expired():
            logger.info("Access token expired or not found. Refreshing token.")
            self.authenticate()
        return self.access_token
