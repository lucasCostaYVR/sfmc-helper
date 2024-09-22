# SFMC Data Extension Lookup

This is a simple Flask web application for interacting with Salesforce Marketing Cloud (SFMC) Data Extensions. Users can look up data from multiple Data Extensions by providing a lookup value. The app retrieves data from SFMC using the SOAP API and displays it in a user-friendly table format.

## Prerequisites

	•	Python 3.7+
	•	Salesforce Marketing Cloud credentials
	•	Flask framework

Setup Instructions

## 1. Clone the Repository

First, clone this repository to your local machine:

```bash
git clone https://github.com/your-username/your-repo.git
cd your-repo
```

## 2. Set Up a Virtual Environment
To keep your dependencies isolated, it’s recommended to set up a virtual environment. You can do this using venv:
```bash
python3 -m venv venv
source venv/bin/activate  # On macOS/Linux
# or
venv\Scripts\activate     # On Windows
```

## 3. Install Dependencies
After activating your virtual environment, install the required dependencies from the requirements.txt file:

```bash
pip install -r requirements.txt
```

## 4. Create the .env File
Create a .env file in the root directory of your project. This file will hold your Salesforce Marketing Cloud credentials and other environment variables.

The .env file should follow this format:

```
CLIENT_ID=yourclientID
CLIENT_SECRET=Yourclientsecre
AUTH_BASE_URL=https://xxxxxx.auth.marketingcloudapis.com/
REST_BASE_URL=https://xxxxxx.rest.marketingcloudapis.com/
SOAP_BASE_URL=https://xxxxxx.soap.marketingcloudapis.com/
FLASK_ENV=development
```

Replace the values with your actual Salesforce Marketing Cloud CLIENT_ID, CLIENT_SECRET, and base URLs.

## 5. Edit lookups.json

The `lookups.json` file contains a list of Data Extensions and their lookup fields. Make sure to update this file with the relevant Data Extensions from your SFMC account. The format of the file should look like this:

```json
[
    {
        "ExternalKey": "SubscriberKeyLookup",
        "LookupField": "SubscriberKey"
    },
    {
        "ExternalKey": "OrderLookup",
        "LookupField": "OrderNumber"
    }
]
```

## 6. Run the Application
Once everything is set up, you can run the Flask app by executing:

```bash
python app.py
```

## 7.Perform Lookups
- Enter a lookup value in the form and click Search.
- The app will retrieve data from the Data Extensions defined in lookups.json and display the results in a table.

## License
This project is licensed under the MIT License.
