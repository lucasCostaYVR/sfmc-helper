# sfmc_helper/automations/automation.py

import logging
from settings import client  # Import the client from settings.py

logger = logging.getLogger(__name__)

TYPE_MAPPING = {
    42: "User-initiated Email",
    43: "Import Definition",
    45: "Group Definition",
    53: "File Transfer Activity",
    73: "Data Extract Activity",
    84: "Report Activity",
    300: "Query Activity",
    303: "Filter Activity",
    423: "Server Side Javascript Activity",
    425: "ELT Activity",
    427: "Build Audience Activity",
    467: "Program Wait",
    724: "Mobile Automation List Refresh Instance",
    725: "MobileConnect Message Instance",
    726: "Mobile File Import Instance",
    733: "InteractionStudio",
    736: "MobilePush Message Object Instance",
    749: "Interaction Studio Event",
    756: "Interaction Studio Date Event",
    771: "Salesforce Send Activity",
    783: "GroupConnect",
    952: "Trigger Journey",
    1010: "Thunderhead Transfer Activity",
    1101: "Interaction Studio Decision Activity",
    1701: "Predictive Intelligence Recommendation Activity"
}

class Automation:
    def __init__(self, id=None):
        self.client = client  # Use the client from settings.py
        self.id = id
        self.name = None
        self.details = {}
        self.steps = []
        if id:
            self.get_details()

    def set_id(self, id):
        if not id:
            raise ValueError("ID is required.")
        self.id = id
        self.get_details()

    @classmethod
    def search_by_name(cls, name: str):
        """
        Searches for Automations by name.

        Args:
            name (str): The name of the Automation to search for.

        Returns:
            list: A list of dictionaries containing details of the Automations.
        """
        filter_string = f"?$filter=name like '{name}'"
        endpoint = 'automation/v1/automations' + filter_string
        response = client.rest_client.get(endpoint)
        try:
            return response.get('items', [])
        except KeyError:
            return []

    def get_details(self):
        if not self.id:
            raise ValueError("ID is required.")
        endpoint = f"automation/v1/automations/{self.id}"
        response = self.client.rest_client.get(endpoint)
        try:
            self.name = response.get('name')
            self.details = response
            steps = [AutomationStep(step['id'], step) for step in response.get('steps', [])]
            self.steps = steps
        except Exception as e:
            logger.error(f"Failed to get automation details: {str(e)}")


class AutomationStep:
    def __init__(self, id, data):
        self.id = id
        self.data = data
        self.step = data.get('step')
        self.name = data.get('name')
        self.activities = []
        # Create instances of the appropriate activity type
        for activity in data.get('activities', []):
            if activity['objectTypeId'] == 300:
                self.activities.append(QueryActivity(activity['id'], activity))
            else:
                self.activities.append(AutomationActivity(activity['id'], activity))


class AutomationActivity:
    def __init__(self, id, data):
        self.id = id
        self.data = data
        self.name = data.get('name')
        self.type = TYPE_MAPPING.get(data.get('objectTypeId'), "Unknown")
        self.target_de = None

        if data.get('targetDataExtensions'):
            self.target_de = data['targetDataExtensions'][0]['name']

    def __str__(self):
        return f"{self.name} ({self.type})"

    def __repr__(self):
        return f"{self.name} ({self.type})"


class QueryActivity(AutomationActivity):
    def __init__(self, id, data):
        super().__init__(id, data)
        self.query = None

        if id:
            self.get_query()

    def get_query(self):
        if not self.query:
            properties = [
                'Name', 'Description', 'CustomerKey', 'QueryText', 'CreatedDate',
                'DataExtensionTarget.Name', 'DataExtensionTarget.CustomerKey', 'ObjectID',
                'TargetType', 'TargetUpdateType'
            ]
            filter = {
                'Property': 'ObjectID',
                'SimpleOperator': 'equals',
                'Value': self.data['activityObjectId']
            }
            response = client.soap_client.retrieve('QueryDefinition', properties, filter)
            results = response.get('soap:Envelope', {}).get('soap:Body', {}).get('RetrieveResponseMsg', {}).get('Results', {})
            if results:
                if isinstance(results, list):
                    result = results[0]
                else:
                    result = results
                self.query = result.get('QueryText')
            else:
                logger.error(f"No QueryDefinition found for ObjectID: {self.data['activityObjectId']}")
                self.query = None

    def __str__(self):
        return f"{self.name} ({self.type}) - {self.query}"

    def __repr__(self):
        return f"{self.name} ({self.type}) - {self.query}"
