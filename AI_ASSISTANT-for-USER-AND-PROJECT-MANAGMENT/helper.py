import difflib
import requests
import json
import os
from dotenv import load_dotenv
load_dotenv()
sso_server_url=os.getenv("sso")
API_BASE_URL_PROJECT = os.getenv("api_base_url_project")

async def verify_authentication(request):
    authorization_header = request.headers.get('Authorization')

    sso_response = requests.get("https://"+sso_server_url+"/api/auth/user", headers={'Authorization': authorization_header})
    print(sso_response)
    try:
        if sso_response.status_code == 200:
            print('ok')
    except requests.exceptions.HTTPError as err:
        # Handle HTTP errors
        return False,1

    sso_response_json = sso_response.json()
    
    if sso_response_json['message'] == 'success':
        return sso_response_json['result'],authorization_header
    else:
        return False,1
    
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)

# Load environment variables
sso_server_url = os.getenv("sso")
if not sso_server_url:
    raise EnvironmentError("SSO_SERVER_URL is not set in the environment variables")

async def verify_authentication(request):
    authorization_header = request.headers.get('Authorization')
    if not authorization_header:
        logging.info("Authorization header is missing")
        return False, 1

    try:
        sso_response = requests.get(f"https://{sso_server_url}/api/auth/user", headers={'Authorization': authorization_header})
        sso_response.raise_for_status()
        sso_response_json = sso_response.json()

        if sso_response_json.get('message') == 'success':
            return sso_response_json.get('result'), authorization_header
        else:
            logging.info("Authentication failed: %s", sso_response_json.get('message'))
            return False, 1
    except requests.exceptions.RequestException as e:
        logging.info("Failed to verify authentication: %s", e)
        return False, 1

def fetch_user_id_from_mobile_no(mobile_no, authorization_header):
    api_url = f"https://{sso_server_url}/api/user"
    headers = {
        'Authorization': authorization_header,
        'Content-Type': 'application/json'
    }
    params = {'key': 'mobile_no', 'value': mobile_no}

    try:
        response = requests.get(api_url, headers=headers, params=params)
        response.raise_for_status()
        data = response.json()

        if data and 'result' in data and data['result']:
            return data['result'][0]['id']
        else:
            logging.info("No user data found in the API response")
    except requests.exceptions.RequestException as e:
        logging.info("Failed to fetch user ID from the API: %s", e)
    except ValueError as e:
        logging.info("Failed to parse JSON response: %s", e)

    return None

def fetch_user_id_from_name(user_name, authorization_header):
    api_url = f"https://{sso_server_url}/api/user"
    headers = {
        'Authorization': authorization_header,
        'Content-Type': 'application/json'
    }

    try:
        response = requests.get(api_url, headers=headers)
        response.raise_for_status()
        data = response.json().get('result', [])

        # Try to find exact matches first
        exact_matches = [user for user in data if f"{user['first_name']} {user['last_name']}".lower() == user_name.lower()]

        if exact_matches:
            return exact_matches

        # If no exact matches, find the closest matches
        full_names = [f"{user['first_name']} {user['last_name']}" for user in data]
        closest_match = difflib.get_close_matches(user_name, full_names, n=1, cutoff=0.0)

        if closest_match:
            closest_matches = [user for user in data if f"{user['first_name']} {user['last_name']}" == closest_match[0]]
            return closest_matches

        logging.info("No close match found for the user name")
    except requests.exceptions.RequestException as e:
        logging.info("Failed to fetch users from the API: %s", e)

    return []

def fetch_role_id_from_api(role_name, authorization_header):
    api_url = f"https://{sso_server_url}/api/roles/"
    headers = {
        'Authorization': authorization_header,
        'Content-Type': 'application/json'
    }

    try:
        response = requests.get(api_url, headers=headers)
        response.raise_for_status()
        data = response.json().get('result', [])

        # Try to find exact match first
        for role in data:
            if role['name'].lower() == role_name.lower():
                return role['id']

        # If no exact match, find the closest match
        role_names = [role['name'] for role in data]
        closest_match = difflib.get_close_matches(role_name, role_names, n=1, cutoff=0.0)

        if closest_match:
            for role in data:
                if role['name'] == closest_match[0]:
                    return role['id']

        logging.info("No close match found for the role name")
    except requests.exceptions.RequestException as e:
        logging.info("Failed to fetch roles from the API: %s", e)

    return None

def fetch_parent_id_from_api(parent_name, authorization_header):
    api_url = f"https://{sso_server_url}/api/user"
    headers = {
        'Authorization': authorization_header,
        'Content-Type': 'application/json'
    }

    try:
        response = requests.get(api_url, headers=headers)
        response.raise_for_status()
        data = response.json().get('result', [])

        # Try to find exact match first
        for user in data:
            full_name = f"{user['first_name']} {user['last_name']}"
            if full_name.lower() == parent_name.lower():
                return user['id']

        # If no exact match, find the closest match
        full_names = [f"{user['first_name']} {user['last_name']}" for user in data]
        closest_match = difflib.get_close_matches(parent_name, full_names, n=1, cutoff=0.0)

        if closest_match:
            for user in data:
                if f"{user['first_name']} {user['last_name']}" == closest_match[0]:
                    return user['id']

        logging.info("No close match found for the parent name")
    except requests.exceptions.RequestException as e:
        logging.info("Failed to fetch users from the API: %s", e)

    return None

def fetch_user_id_from_api(user_name, authorization_header):
    api_url = f"https://{sso_server_url}/api/user"
    headers = {
        'Authorization': authorization_header,
        'Content-Type': 'application/json'
    }

    try:
        response = requests.get(api_url, headers=headers)
        response.raise_for_status()
        data = response.json().get('result', [])

        # Try to find exact match first
        for user in data:
            full_name = f"{user['first_name']} {user['last_name']}"
            if full_name.lower() == user_name.lower():
                return user['id']

        # If no exact match, find the closest match
        full_names = [f"{user['first_name']} {user['last_name']}" for user in data]
        closest_match = difflib.get_close_matches(user_name, full_names, n=1, cutoff=0.0)

        if closest_match:
            for user in data:
                if f"{user['first_name']} {user['last_name']}" == closest_match[0]:
                    return user['id']

        logging.info("No close match found for the user name")
    except requests.exceptions.RequestException as e:
        logging.info("Failed to fetch users from the API: %s", e)

    return None

def get_project_ids(user_name, project_name, authorization_header):
    user_id = fetch_user_id_from_api(user_name, authorization_header)
    if not user_id:
        logging.info("User ID not found")
        return []

    url = f"https://{API_BASE_URL_PROJECT}/search"
    payload = json.dumps({
        "query": project_name,
        "fields_to_search": ["project"]
    })
    headers = {
        'Accept': 'application/json',
        'Authorization': authorization_header,
        'Content-Type': 'application/json'
    }

    try:
        response = requests.post(url, headers=headers, data=payload)
        response.raise_for_status()
        response_data = response.json()
        ids = [item['_id'] for item in response_data.get('result', []) if item['user_id'] == str(user_id)]
        return ids
    except requests.exceptions.RequestException as e:
        logging.info("Failed to fetch project IDs from the API: %s", e)

    return []

def get_project_parent_id(project_name, authorization_header):
    url = f"https://{API_BASE_URL_PROJECT}/search"
    payload = json.dumps({
        "query": project_name,
        "fields_to_search": ["name"]
    })
    headers = {
        'Accept': 'application/json',
        'Authorization': authorization_header,
        'Content-Type': 'application/json'
    }

    try:
        response = requests.post(url, headers=headers, data=payload)
        response.raise_for_status()
        response_data = response.json()
        if response_data.get('result', []):
            first_result = response_data['result'][0]
            return first_result['name'], first_result['_id']
        else:
            logging.info("No projects found matching the name")
    except requests.exceptions.RequestException as e:
        logging.info("Failed to fetch project parent ID from the API: %s", e)

    return None, None
