import requests
import time

class BaseClient:
    """
    A base class for authentication for the SFMC API.
    """
    def __init__(self, client_id, client_secret,auth_base_url):
        self.client_id = client_id
        self.client_secret = client_secret
        self.auth_base_url = auth_base_url
        self.access_token = None
        self.token_expiry = None
        self.authenticate()

    def authenticate(self):
        """
        Authenticate with the SFMC API.
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
            self.token_expiry = time.time() + data['expires_in']
        except requests.exceptions.RequestException as e:
            raise SystemExit(e)
        
    def is_token_expired(self):
        """
        Check if the token is expired.
        """
        return self.token_expiry is not None and time.time() >= self.token_expiry
    
    def get_access_token(self):
        """
        Retrieves a valid access token, refreshing it if necessary.

        Returns:
            str: The valid access token.
        """
        if self.access_token is None or self.is_token_expired():
            self.authenticate()
        return self.access_token
        

