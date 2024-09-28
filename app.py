from flask import Flask, render_template, request, redirect, url_for, flash
from sfmc_helper.data_extensions.data_extension import DataExtension
from sfmc_helper.automations.automation import Automation
from sfmc_helper.filters.filters import SimpleFilter
import json
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with a secure random key

# Load lookups.json
def load_lookups():
    with open('lookups.json', 'r') as f:
        return json.load(f)

# Save lookups.json
def save_lookups(lookups):
    with open('lookups.json', 'w') as f:
        json.dump(lookups, f, indent=4)

@app.route('/', endpoint='home')
def home():
    return redirect(url_for('lookup'))

# Home page to render the lookup form
@app.route('/lookup')
def lookup():
    return render_template('index.html')

# Handle form submission, loop through lookups, and display the results
@app.route('/lookup/results', methods=['POST'])
def results():
    lookup_value = request.form.get('lookup_value')

    # Load lookups from JSON
    lookups = load_lookups()

    # Loop through each lookup and retrieve the data
    results = []
    for lookup in lookups:
        de = DataExtension(lookup['ExternalKey'])

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

@app.route('/auomation-docs', endpoint='automation-docs', methods=['GET', 'POST'])
def automation_docs():
    if request.method == 'POST':
        automation_name = request.form.get('automation_name')
        automations = Automation.search_by_name(automation_name)
        context = {
            'automation_name': automation_name,
            'automations': automations
        }
        return render_template('automation_docs_results.html', **context)

    return render_template('automation_docs.html')

@app.route('/automation-docs/<automation_id>', methods=['GET'], endpoint='automation-details')
def automation_details(automation_id):
    automation = Automation(automation_id)
    context = {
        'automation': automation
    }
    return render_template('automation_details.html', **context)

if __name__ == '__main__':
    app.run(debug=True)
