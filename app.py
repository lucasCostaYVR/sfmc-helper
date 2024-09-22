from flask import Flask, render_template, request, redirect, url_for
from sfmc_helper.data_extensions.data_extension import DataExtension
from sfmc_helper.auth.client import SFMCClient
from sfmc_helper.filters.filters import SimpleFilter
import json
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

client = SFMCClient(
    client_id=os.getenv('CLIENT_ID'),
    client_secret=os.getenv('CLIENT_SECRET'),
    auth_base_url=os.getenv('AUTH_BASE_URL'),
    rest_base_url=os.getenv('REST_BASE_URL'),
    soap_base_url=os.getenv('SOAP_BASE_URL')
)

# Load lookups.json
def load_lookups():
    with open('lookups.json') as f:
        return json.load(f)

# Home page to render the lookup form
@app.route('/')
def index():
    return render_template('index.html')

# Handle form submission, loop through lookups, and display the results
@app.route('/results', methods=['POST'])
def results():
    lookup_value = request.form.get('lookup_value')
    
    # Load lookups from JSON
    lookups = load_lookups()

    # Loop through each lookup and retrieve the data
    results = []
    for lookup in lookups:
        de = DataExtension(client, lookup['ExternalKey'])
        
        # Use the lookup field defined in the JSON file for the filter
        filter = SimpleFilter(lookup['LookupField'], 'equals', lookup_value)
        
        # Retrieve data for each Data Extension
        data = de.data(filter=filter)
        
        # Add the results along with the name of the Data Extension
        results.append({
            'external_key': lookup['ExternalKey'],
            'data': data
        })
    
    # Render the results page with the retrieved data
    return render_template('results.html', results=results, lookup_value=lookup_value)

if __name__ == '__main__':
    app.run(debug=True)