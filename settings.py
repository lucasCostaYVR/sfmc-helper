# settings.py
from sfmc_helper.auth.client import SFMCClient
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

client = SFMCClient(
    client_id=os.getenv('CLIENT_ID'),
    client_secret=os.getenv('CLIENT_SECRET'),
    auth_base_url=os.getenv('AUTH_BASE_URL'),
    rest_base_url=os.getenv('REST_BASE_URL'),
    soap_base_url=os.getenv('SOAP_BASE_URL')
)
