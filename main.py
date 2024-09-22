
from sfmc_helper.auth.client import SFMCClient
from sfmc_helper.data_extensions.data_extension import DataExtension
from sfmc_helper.filters.filters import SimpleFilter, ComplexFilter, LogicalOperator, SimpleOperator
import os
from dotenv import load_dotenv

load_dotenv()

client = SFMCClient(
    client_id=os.getenv('CLIENT_ID'),
    client_secret=os.getenv('CLIENT_SECRET'),
    auth_base_url=os.getenv('AUTH_BASE_URL'),
    rest_base_url=os.getenv('REST_BASE_URL'),
    soap_base_url=os.getenv('SOAP_BASE_URL')
)

skl = DataExtension(client, 'SubscriberKeyLookup')
fields = skl.fields
for field in fields:
    print(field['Name'])

primary_keys = skl.primary_keys
print(primary_keys)
filter = SimpleFilter('EmailAddress', 'equals', 'lcosta@lululemon.com')
data = skl.data(filter=filter)
print(data)












