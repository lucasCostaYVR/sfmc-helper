import requests
import logging
import time
import xmltodict
from sfmc_helper.auth.base_client import BaseClient

# Configure logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

class SoapClient(BaseClient):
    """
    A client for interacting with the SFMC SOAP API using requests instead of Zeep.
    """

    def __init__(self, client_id, client_secret, auth_base_url, soap_base_url):
        """
        Initializes the SoapClient with authentication details and SOAP settings.

        Args:
            client_id (str): Your SFMC client ID.
            client_secret (str): Your SFMC client secret.
            auth_base_url (str): The base URL for authentication.
            soap_base_url (str): The base URL for the SOAP API.
        """
        super().__init__(client_id, client_secret, auth_base_url)
        self.soap_base_url = soap_base_url.rstrip('/') + "/Service.asmx"

    def _build_soap_envelope(self, method: str, body_xml: str) -> str:
        """
        Builds the SOAP envelope for the given method and body XML.

        :param method: The SOAP action (e.g., Retrieve, Create).
        :param body_xml: The XML body content for the SOAP request.
        :return: A string representing the full SOAP envelope.
        """
        envelope = f"""<?xml version="1.0" encoding="UTF-8"?>
        <s:Envelope xmlns:s="http://www.w3.org/2003/05/soap-envelope" xmlns:a="http://schemas.xmlsoap.org/ws/2004/08/addressing" xmlns:u="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-utility-1.0.xsd">
            <s:Header>
                <a:Action s:mustUnderstand="1">{method}</a:Action>
                <a:To s:mustUnderstand="1">{self.soap_base_url}</a:To>
                <fueloauth xmlns="http://exacttarget.com">{self.get_access_token()}</fueloauth>
            </s:Header>
            <s:Body xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema">
                {body_xml}
            </s:Body>
        </s:Envelope>"""
        return envelope

    def _make_soap_request(self, method: str, body_xml: str) -> dict:
        """
        Makes a SOAP request to the SFMC API.

        :param method: The SOAP action (e.g., Retrieve, Create).
        :param body_xml: The XML body content for the SOAP request.
        :return: A dictionary parsed from the XML response.
        """
        headers = {
            "Content-Type": "text/xml; charset=utf-8",
            "SOAPAction": method,
        }

        # Build the SOAP envelope
        soap_envelope = self._build_soap_envelope(method, body_xml)

        # Make the request
        response = requests.post(self.soap_base_url, data=soap_envelope, headers=headers)
        response.raise_for_status()

        # Parse the response from XML to dict
        return xmltodict.parse(response.content)

    def retrieve(self, object_type: str, properties: list[str], filter: dict = None) -> dict:
        """
        Retrieves objects of the specified type from the SFMC SOAP API.

        :param object_type: The type of object to retrieve (e.g., 'Subscriber').
        :param properties: A list of property names to retrieve.
        :param filter: A filter for the retrieve operation (optional).
        :return: The SOAP response as a dictionary.
        """
        properties_xml = "".join([f"<Properties>{prop}</Properties>" for prop in properties])

        filter_xml = ""
        if filter:
            filter_xml = f"""
            <Filter xsi:type="SimpleFilterPart">
                <Property>{filter['Property']}</Property>
                <SimpleOperator>{filter['SimpleOperator']}</SimpleOperator>
                <Value>{filter['Value']}</Value>
            </Filter>
            """

        body_xml = f"""
        <RetrieveRequestMsg xmlns="http://exacttarget.com/wsdl/partnerAPI">
            <RetrieveRequest>
                <ObjectType>{object_type}</ObjectType>
                {properties_xml}
                {filter_xml}
            </RetrieveRequest>
        </RetrieveRequestMsg>
        """

        return self._make_soap_request("Retrieve", body_xml)

    def create(self, objects: list[dict]) -> dict:
        """
        Creates objects in SFMC via the SOAP API.

        :param objects: A list of objects to create.
        :return: The SOAP response as a dictionary.
        """
        # Construct the XML for objects to create
        objects_xml = "".join([
            f"<Objects><CustomerKey>{obj['CustomerKey']}</CustomerKey><Name>{obj['Name']}</Name></Objects>" for obj in objects
        ])

        body_xml = f"""
        <CreateRequest xmlns="http://exacttarget.com/wsdl/partnerAPI">
            {objects_xml}
        </CreateRequest>
        """

        return self._make_soap_request("Create", body_xml)

    def update(self, objects: list[dict]) -> dict:
        """
        Updates objects in SFMC via the SOAP API.

        :param objects: A list of objects to update.
        :return: The SOAP response as a dictionary.
        """
        objects_xml = "".join([
            f"<Objects><CustomerKey>{obj['CustomerKey']}</CustomerKey><Name>{obj['Name']}</Name></Objects>" for obj in objects
        ])

        body_xml = f"""
        <UpdateRequest xmlns="http://exacttarget.com/wsdl/partnerAPI">
            {objects_xml}
        </UpdateRequest>
        """

        return self._make_soap_request("Update", body_xml)

    def delete(self, objects: list[dict]) -> dict:
        """
        Deletes objects in SFMC via the SOAP API.

        :param objects: A list of objects to delete.
        :return: The SOAP response as a dictionary.
        """
        objects_xml = "".join([
            f"<Objects><CustomerKey>{obj['CustomerKey']}</CustomerKey><Name>{obj['Name']}</Name></Objects>" for obj in objects
        ])

        body_xml = f"""
        <DeleteRequest xmlns="http://exacttarget.com/wsdl/partnerAPI">
            {objects_xml}
        </DeleteRequest>
        """

        return self._make_soap_request("Delete", body_xml)