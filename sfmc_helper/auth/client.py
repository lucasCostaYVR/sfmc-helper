from sfmc_helper.auth.rest_client import RestClient
from sfmc_helper.auth.soap_client import SoapClient



class SFMCClient:
    """
    A client for interacting with the SFMC API.Encpasulates the REST and SOAP clients.
    """
    def __init__(self, client_id, client_secret, auth_base_url, rest_base_url, soap_base_url):
        self.rest_client = RestClient(client_id, client_secret, auth_base_url, rest_base_url)
        self.soap_client = SoapClient(client_id, client_secret, auth_base_url, soap_base_url)

    def get_access_token(self):
        """
        Retrieves a valid access token from the REST client.

        Returns:
            str: The valid access token.
        """
        return self.rest_client.get_access_token()
    
    def get_rest_endpoints(self):
        """
        Retrieves the REST endpoints from the REST client.

        Returns:
            dict: The REST endpoints.
        """
        return self.rest_client.get('platform/v1/endpoints')
    
    

