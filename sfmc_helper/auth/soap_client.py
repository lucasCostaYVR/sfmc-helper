# soap_client.py
import requests
import logging
import xmltodict
from sfmc_helper.auth.base_client import BaseClient

# Configure logging
logger = logging.getLogger(__name__)

class SoapClient(BaseClient):
    """
    A client for interacting with the SFMC SOAP API using requests.
    """
    def __init__(self, client_id, client_secret, auth_base_url, soap_base_url):
        super().__init__(client_id, client_secret, auth_base_url)
        self.soap_base_url = soap_base_url.rstrip('/') + "/Service.asmx"

    def _build_soap_envelope(self, method: str, body_xml: str) -> str:
        """
        Builds the SOAP envelope for the given method and body XML.
        """
        envelope = f"""<?xml version="1.0" encoding="UTF-8"?>
    <s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/"
                xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
                xmlns:xsd="http://www.w3.org/2001/XMLSchema">
        <s:Header>
            <fueloauth xmlns="http://exacttarget.com">{self.get_access_token()}</fueloauth>
        </s:Header>
        <s:Body>
            {body_xml}
        </s:Body>
    </s:Envelope>"""
        return envelope

    def _make_soap_request(self, method: str, body_xml: str) -> dict:
        """
        Makes a SOAP request to the SFMC API.
        """
        headers = {
            "Content-Type": "text/xml; charset=utf-8",
            "SOAPAction": f"{method}"
        }

        # Build the SOAP envelope
        soap_envelope = self._build_soap_envelope(method, body_xml)

        # Make the request
        try:
            response = requests.post(self.soap_base_url, data=soap_envelope, headers=headers)
            response.raise_for_status()
            # Parse the response from XML to dict
            return xmltodict.parse(response.content)
        except requests.exceptions.RequestException as e:
            logger.error(f"SOAP {method} request failed: {e}")
            raise

    def retrieve(self, object_type: str, properties: list, filter: dict = None) -> dict:
        """
        Retrieves objects of the specified type from the SFMC SOAP API.
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
        # Make sure the 'xmlns:xsi' is declared in the root element or the element where it's used

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

    # Additional methods (create, update, delete) can be implemented similarly
