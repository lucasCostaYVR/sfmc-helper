# data_extension.py

import logging
from typing import Union
from sfmc_helper.filters.filters import SimpleFilter, ComplexFilter
from settings import client  # Import the client from settings.py

logger = logging.getLogger(__name__)

class DataExtension:
    """
    A class for interacting with SFMC Data Extensions.
    """

    def __init__(self, external_key: str = None):
        self.client = client  # Use the client from settings.py
        self.external_key = external_key
        self.name = None
        self.details = {}
        self.fields = []
        self.primary_keys = []
        if external_key:
            self.details = self.__get_details()
            self.fields = self.__get_fields()

    def set_external_key(self, external_key: str):
        """
        Sets the external key of the Data Extension.

        Args:
            external_key (str): The external key of the Data Extension.
        """
        self.external_key = external_key
        self.details = self.__get_details()
        self.fields = self.__get_fields()

    def __get_fields(self):
        """
        Retrieves the fields of the Data Extension.

        Returns:
            list: A list of dictionaries containing Data Extension fields.
        """
        object_type = 'DataExtensionField'
        properties = ['Name', 'FieldType', 'IsPrimaryKey', 'IsRequired', 'MaxLength']
        filter = {
            'Property': 'DataExtension.CustomerKey',
            'SimpleOperator': 'equals',
            'Value': self.external_key
        }

        response = self.client.soap_client.retrieve(object_type, properties, filter)

        # Handling the response and extracting 'Results' from the 'soap:Body'
        results = response.get('soap:Envelope', {}).get('soap:Body', {}).get('RetrieveResponseMsg', {}).get('Results', None)
        logger.info(f"Data Extension fields: {results}")

        if results:
            # Ensure results is a list
            if not isinstance(results, list):
                results = [results]

            for result in results:
                if result.get('IsPrimaryKey', 'false') == 'true':
                    self.primary_keys.append(result.get('Name'))
            return results
        else:
            logger.error(f"No fields found for Data Extension with CustomerKey: {self.external_key}")
            return []

    def __get_details(self):
        """
        Retrieves the details of the Data Extension.

        Returns:
            dict: A dictionary containing Data Extension details.
        """
        object_type = 'DataExtension'
        properties = ['CustomerKey', 'Name', 'IsSendable', 'IsTestable']
        filter = {
            'Property': 'CustomerKey',
            'SimpleOperator': 'equals',
            'Value': self.external_key
        }

        response = self.client.soap_client.retrieve(object_type, properties, filter)

        logger.info(f"Data Extension details: {response}")

        # Handling the response and extracting 'Results' from the 'soap:Body'
        results = response.get('soap:Envelope', {}).get('soap:Body', {}).get('RetrieveResponseMsg', {}).get('Results', None)
        logger.info(f"Data Extension results: {results}")

        if results:
            # Ensure results is a dictionary
            if isinstance(results, list):
                results = results[0]  # Take the first result if multiple exist
            self.name = results.get('Name')
            return results
        else:
            logger.error(f"No Data Extension found with CustomerKey: {self.external_key}")
            return {}

    def data(self, filter: Union[SimpleFilter, ComplexFilter, None] = None):
        """
        Retrieves data from the Data Extension based on the specified filter.

        Args:
            filter (SimpleFilter | ComplexFilter | None): A filter to apply to the data retrieval.
        Returns:
            list: A list of dictionaries representing rows of data.
        """
        # Ensure the external key is set
        if not self.external_key:
            raise ValueError("External key is not set. Please set it using set_external_key.")

        # Retrieve properties (fields) from the Data Extension
        properties_xml = "".join(f'<Properties>{field["Name"]}</Properties>' for field in self.fields)
        properties_xml += "<Properties>_CustomObjectKey</Properties>"

        # Build the filter XML if a filter is provided
        filter_xml = ""
        if filter:
            filter_xml = filter.to_xml()

        # Construct the SOAP request body
        body_xml = f"""
        <RetrieveRequestMsg xmlns="http://exacttarget.com/wsdl/partnerAPI">
            <RetrieveRequest>
                <ObjectType>DataExtensionObject[{self.name}]</ObjectType>
                {properties_xml}
                {filter_xml}
            </RetrieveRequest>
        </RetrieveRequestMsg>
        """

        # Make the SOAP request using the SoapClient
        response = self.client.soap_client._make_soap_request("Retrieve", body_xml)

        # Extract and handle the response
        if (
            "soap:Envelope" in response
            and "soap:Body" in response["soap:Envelope"]
            and "RetrieveResponseMsg" in response["soap:Envelope"]["soap:Body"]
            and "Results" in response["soap:Envelope"]["soap:Body"]["RetrieveResponseMsg"]
        ):
            raw_results = response["soap:Envelope"]["soap:Body"]["RetrieveResponseMsg"]["Results"]
        else:
            raw_results = []

        # Handle cases where results might be a single dict instead of a list
        if not isinstance(raw_results, list):
            raw_results = [raw_results]

        # Parse the raw results into a more usable format
        parsed_data = []
        for row in raw_results:
            row_dict = {}
            properties = row.get("Properties", {}).get("Property", [])
            # Ensure properties is a list
            if isinstance(properties, dict):
                properties = [properties]
            for item in properties:
                row_dict[item["Name"]] = item.get("Value")
            parsed_data.append(row_dict)

        return parsed_data
