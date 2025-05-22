import difflib
import requests
import json
import os
import traceback
from dotenv import load_dotenv
load_dotenv()
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)

sso_server_url = os.getenv("sso")
url = os.getenv("url")
dynamicurls = os.getenv("dynamicurl")
crudurl = os.getenv("crudurl")

if not sso_server_url:
    raise EnvironmentError("SSO_SERVER_URL is not set in the environment variables")

async def verify_authentications(authorization_header):
    if not authorization_header:
        logging.error("Authorization header is missing")
        return False, 1

    try:
        sso_response = requests.get(f"https://{sso_server_url}/api/auth/user", headers={'Authorization': authorization_header})
        sso_response.raise_for_status()
        sso_response_json = sso_response.json()

        if sso_response_json.get('message') == 'success':
            return sso_response_json.get('result'), authorization_header
        else:
            logging.error("Authentication failed: %s", sso_response_json.get('message'))
            return False, 1
    except requests.exceptions.RequestException as e:
        logging.error("Failed to verify authentication: %s", e)
        logging.error(traceback.format_exc())
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
        logging.error("Failed to fetch user ID from the API: %s", e)
        logging.error(traceback.format_exc())
    except ValueError as e:
        logging.error("Failed to parse JSON response: %s", e)
        logging.error(traceback.format_exc())

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

        # Normalize the user name for matching
        normalized_user_name = user_name.lower().strip()

        # Split the user name into first and last names
        user_name_parts = normalized_user_name.split()
        if len(user_name_parts) < 1:
            logging.error("User name must contain at least a first name.")
            return []

        first_name = user_name_parts[0]
        last_name = user_name_parts[1] if len(user_name_parts) > 1 else None

        # List to hold potential matches based on the first name
        potential_matches = []

        for user in data:
            user_first_name = user['first_name'].lower()
            user_last_name = user['last_name'].lower() if user['last_name'] else ''

            full_name = f"{user['first_name']} {user['last_name']}".lower()

            # Exact match by full name
            if full_name == normalized_user_name:
                return [user]

            # Match first name
            if first_name == user_first_name:
                potential_matches.append(user)

        # If last name is provided, further refine potential matches
        if last_name:
            final_matches = [user for user in potential_matches if user['last_name'] and user['last_name'].lower() == last_name]
            if final_matches:
                return final_matches
        else:
            # If only the first name is provided and we have multiple matches, return all of them
            if potential_matches:
                return potential_matches

        # If no matches are found, attempt to find the closest match using difflib
        full_names = [f"{user['first_name']} {user['last_name']}".lower() for user in data]
        closest_match = difflib.get_close_matches(normalized_user_name, full_names, n=1, cutoff=0.6)

        if closest_match:
            closest_matches = [user for user in data if f"{user['first_name']} {user['last_name']}".lower() == closest_match[0]]
            return closest_matches

        logging.info("No close match found for the user name")
        return []

    except requests.exceptions.RequestException as e:
        logging.error(f"Failed to fetch users from the API: {e}")
        logging.error(traceback.format_exc())
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

            logging.info(f"List of Roles: {[role['name'] for role in data]}")

            if role['name'].lower() == role_name.lower():
                return role['id']

        # If no exact match, find the closest match
        role_names = [role['name'] for role in data]

        logging.info(f"List of Roles: {role_names}")
        closest_match = difflib.get_close_matches(role_name, role_names, n=1, cutoff=0.6)
        logging.info(f"Closest matching role is: {closest_match}")


        if closest_match:
            for role in data:
                if role['name'] == closest_match[0]:
                    return role['id']

        logging.debug("No close match found for the role name")
    except requests.exceptions.RequestException as e:
        logging.error("Failed to fetch roles from the API: %s", e)
        logging.error(traceback.format_exc())

    return None


def fetch_parent_id_from_api(team_leader, designation,authorization_header):
    try:
        if designation.lower() == "sub team leader":
            api_url = "https://ssodev.evoluxar.com/api/user_dropdown_list/?designation=Team%20Leader"
        elif designation.lower() == "executive":
            api_url = "https://ssodev.evoluxar.com/api/user_dropdown_list/?designation=Team%20Leader%2CSub%20Team%20Leader"
        else:
            api_url = f"https://{sso_server_url}/api/user"
        
        headers = {
            'Authorization': authorization_header,
            'Content-Type': 'application/json'
        }
        response = requests.get(api_url, headers=headers)
        response.raise_for_status()
        data = response.json().get('result', [])

        # Normalize the parent name for matching
        normalized_team_leader = team_leader.lower().strip()

        # Split the parent name into first and last names
        team_leader_parts = normalized_team_leader.split()
        if len(team_leader_parts) < 1:
            logging.error("Parent name must contain at least a first name.")
            return None

        first_name = team_leader_parts[0]
        last_name = team_leader_parts[1] if len(team_leader_parts) > 1 else None

        # List to hold potential matches
        potential_matches = []

        for user in data:
            user_first_name = user['first_name'].lower()
            user_last_name = user['last_name'].lower() if user['last_name'] else ''

            full_name = f"{user['first_name']} {user['last_name']}".lower()
            if full_name == normalized_team_leader:
                return user['id']

            if first_name == user_first_name:
                potential_matches.append(user)

        if last_name:
            for user in potential_matches:
                if user['last_name'] and user['last_name'].lower() == last_name:
                    return user['id']
        else:
            if len(potential_matches) == 1:
                return potential_matches[0]['id']
            elif len(potential_matches) > 1:
                logging.error("Multiple users with the same first name found. Please provide the last name.")
                return None
            else:
                full_names = [f"{user['first_name']} {user['last_name']}".lower() for user in data]
                closest_match = difflib.get_close_matches(normalized_team_leader, full_names, n=1, cutoff=0.6)

                if closest_match:
                    for user in data:
                        if f"{user['first_name']} {user['last_name']}".lower() == closest_match[0]:
                            return user['id']

                logging.info("No close match found for the team_leader name")
                return None

    except requests.exceptions.RequestException as e:
        logging.error("Failed to fetch users from the API: %s", e)
        logging.error(traceback.format_exc())

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
        
        # Normalize the username for matching
        normalized_user_name = user_name.lower().strip()

        # Split the username  into first and last names
        user_name_parts = normalized_user_name.split()
        if len(user_name_parts) < 1:
            logging.error("Parent name must contain at least a first name.")
            return None

        first_name = user_name_parts[0]
        last_name = user_name_parts[1] if len(user_name_parts) > 1 else None

        # List to hold potential matches
        potential_matches = []

        for user in data:
            user_first_name = user['first_name'].lower()
            user_last_name = user['last_name'].lower() if user['last_name'] else ''

            full_name = f"{user['first_name']} {user['last_name']}".lower()
            if full_name == normalized_user_name:
                return user['id']

            if first_name == user_first_name:
                potential_matches.append(user)

        if last_name:
            for user in potential_matches:
                if user['last_name'] and user['last_name'].lower() == last_name:
                    return user['id']
        else:
            if len(potential_matches) == 1:
                return potential_matches[0]['id']
            elif len(potential_matches) > 1:
                logging.error("Multiple users with the same first name found. Please provide the last name.")
                return None
            else:
                full_names = [f"{user['first_name']} {user['last_name']}".lower() for user in data]
                closest_match = difflib.get_close_matches(normalized_user_name, full_names, n=1, cutoff=0.6)

                if closest_match:
                    for user in data:
                        if f"{user['first_name']} {user['last_name']}".lower() == closest_match[0]:
                            return user['id']

                logging.info("No close match found for the team_leader name")
                return None

    except requests.exceptions.RequestException as e:
        logging.error("Failed to fetch users from the API: %s", e)
        logging.error(traceback.format_exc())

    return None

    #     for user in data:
    #         full_name = f"{user['first_name']} {user['last_name']}"
    #         if full_name.lower() == user_name.lower():
    #             return user['id']

    #     full_names = [f"{user['first_name']} {user['last_name']}" for user in data]
    #     closest_match = difflib.get_close_matches(user_name, full_names, n=1, cutoff=0.6)

    #     if closest_match:
    #         for user in data:
    #             if f"{user['first_name']} {user['last_name']}" == closest_match[0]:
    #                 return user['id']

    #     logging.info("No close match found for the user name")
    # except requests.exceptions.RequestException as e:
    #     logging.error("Failed to fetch users from the API: %s", e)
    #     logging.error(traceback.format_exc())

    # return None

def get_project_ids(user_name, project_name, authorization_header):
    user_id = fetch_user_id_from_api(user_name, authorization_header)
    if not user_id:
        logging.info("User ID not found")
        return []

    url = "https://"+str(dynamicurls)+"/projectassignment/search"
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
        logging.error("Failed to fetch project IDs from the API: %s", e)
        logging.error(traceback.format_exc())

    return []

def get_project_parent_id(project_name, authorization_header):
    url = "https://"+str(dynamicurls)+"/projects/search"
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
        logging.error("Failed to fetch project parent ID from the API: %s", e)
        logging.error(traceback.format_exc())

    return None, None

def fetch_business_name_from_api(business, authorization_header):
    url = f"https://{crudurl}/api/business/"
    
    headers = {
        'Authorization': authorization_header,
        'Content-Type': 'application/json'
    }

    try:
        logging.info(f"Fetching from URL: {url}")
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json().get('result', [])

        # Normalize the business name for matching
        normalized_business_name = business.lower().strip()
        business_names = [business['name'] for business in data]

        # First, try to find an exact match
        for business in data:
            if normalized_business_name == business['name'].lower().strip():
                return business['name']

        # If no exact match is found, use fuzzy matching
        closest_matches = difflib.get_close_matches(normalized_business_name, business_names, n=1, cutoff=0.6)

        if closest_matches:
            for business in data:
                if business['name'] == closest_matches[0]:
                    return business['name']

        logging.info("No close match found for the business name")
    except requests.exceptions.RequestException as e:
        logging.error("Failed to fetch businesses from the API: %s", e)
        logging.error(traceback.format_exc())

    return None
