import unittest
from unittest.mock import patch
from sfmc_helper.rest.rest_client import RestClient

class TestRestClient(unittest.TestCase):
    def setUp(self) -> None:
        self.client_id = 'my_client_id',
        self.client_secret = 'my_client_secret',
        self.auth_base_url = 'https://auth.exacttargetapis.com',
        self.rest_base_url = 'https://rest.exacttargetapis.com'
        self.client = RestClient(
            client_id=self.client_id,
            client_secret=self.client_secret,
            auth_base_url=self.auth_base_url,
            rest_base_url=self.rest_base_url
        )

        @patch('sfmc_helper.rest.rest_client.get')
        @patch('sfmc_helper.rest.rest_client.post')
        def test_get_method_success(self, mock_get, mock_post):
            """
            Test the get method of the RestClient class.
            """

if __name__ == '__main__':
    unittest.main()