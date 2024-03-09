import requests
from requests.auth import HTTPBasicAuth
import json
from pylogix import PLC

# PLC A - replace IP's and Tag names
LOCATION_A_PLC = PLC()
LOCATION_A_PLC.IPAddress = '10.0.0.1'
LOCATION_A_PLC.ProcessorSlot = 0
LOCATION_A_PLC_RESULT = LOCATION_A_PLC.Read('TagNameHere')
LOCATION_A_VALUE = LOCATION_A_PLC_RESULT.Value

# PLC B
LOCATION_B_PLC = PLC()
LOCATION_B_PLC.IPAddress = '10.0.0.2'
LOCATION_B_PLC.ProcessorSlot = 0
LOCATION_B_PLC_RESULT = LOCATION_B_PLC.Read('TagNameHere')
LOCATION_B_VALUE = LOCATION_B_PLC_RESULT.Value

# PLC C
LOCATION_C_PLC = PLC()
LOCATION_C_PLC.IPAddress = '10.0.0.3'
LOCATION_C_PLC.ProcessorSlot = 0
LOCATION_C_PLC_RESULT = LOCATION_C_PLC.Read('TagNameHere')
LOCATION_C_VALUE = LOCATION_C_PLC_RESULT.Value

# PLC D
LOCATION_D_PLC = PLC()
LOCATION_D_PLC.IPAddress = '10.0.0.4'
LOCATION_D_PLC.ProcessorSlot = 0
LOCATION_D_PLC_RESULT = LOCATION_D_PLC.Read('TagNameHere')
LOCATION_D_VALUE = LOCATION_D_PLC_RESULT.Value

#PLC value in a dictionary
plc_dict = {
    'Location A': LOCATION_A_VALUE,
    'Location B': LOCATION_B_VALUE,
    'Location C': LOCATION_C_VALUE,
    'Location D': LOCATION_D_VALUE,
}

#Value check
under_30k_dict = {}
for var_name, value in plc_dict.items():
    if value < 30000:
        under_30k_dict[var_name] = value

#converts the under_30k dictionary into a list for better formatting in email
email_body_data = [f"{key}: {value}" for key, value in under_30k_dict.items()]

#If there are any values in the under_30k dictionary, send an email with a list of all locations and values
if under_30k_dict:
    print(under_30k_dict)
    # Variables Required to connect to Azure tennant
    client_id = 'Client ID goes here'
    client_secret = 'Client secret goes here'
    tenant_id = 'Tenant ID goes here'
    scope = 'https://graph.microsoft.com/.default'
    grant_type = 'client_credentials'
    token_url = f'https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0/token'
    mail_url = 'https://graph.microsoft.com/v1.0/users/username@outlook.com/APINAME' #replace email and API name

    # Get an access token
    token_data = {
        'grant_type': grant_type,
        'client_id': client_id,
        'client_secret': client_secret,
        'scope': scope,
    }

    token_r = requests.post(token_url, data=token_data)
    token = token_r.json().get('access_token')

    # Use the access token to send an email
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }


    email_data = {
        "message": {
            "subject": f', '.join(email_body_data),
            "body": {
                "contentType": "Text",
                "content": f', '.join(email_body_data),
            },
            "toRecipients": [
                {
                    "emailAddress": {
                        "address": "user1@outlook.com"
                    }
                },
                {
                    "emailAddress": {
                        "address": "user2@outlook.com"
                    }
            ],
            "ccRecipients": [
                {
                    "emailAddress": {
                        "address": "user3@gmail.com"
                    }
                },
                {
                    "emailAddress": {
                        "address": "user4@gmail.com"
                    }
                }
            ]
        },
        "saveToSentItems": "true"
    }

    response = requests.post(mail_url, headers=headers, json=email_data)

    #Remove comments while testing to verify it works
    # if response.status_code == 202:
    #     print("Email sent successfully!")
    # else:
    #     print(f"Failed to send email: {response.status_code}")
    #     print(response.json())
