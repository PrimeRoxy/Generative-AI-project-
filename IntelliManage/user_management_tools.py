import difflib
import os
from datetime import datetime
import traceback
import aiohttp
from dotenv import load_dotenv
import httpx
import json
import logging

import requests
from .helper import fetch_business_name_from_api, fetch_parent_id_from_api, fetch_role_id_from_api, fetch_user_id_from_api, fetch_user_id_from_mobile_no, fetch_user_id_from_name, get_project_ids, get_project_parent_id

load_dotenv()
urls = os.getenv("url")
sso = os.getenv("sso")
dynamicurls = os.getenv("dynamicurl")
crudurl = os.getenv("crudurl")

# Configure logging
logging.basicConfig(level=logging.INFO)

async def create_user_tool(first_name, last_name, mobile_no, email, team_leader, role_name, business,designation, authorization_header, pan_no=None, aadhar_no=None):
    # import pdb; pdb.set_trace()
    try:
        parent_id = fetch_parent_id_from_api(team_leader, designation, authorization_header)

        if not parent_id:
            return f"No team leader name matches for '{team_leader}'. Please provide the correct or full name of the team leader."

        role_id = fetch_role_id_from_api(role_name, authorization_header)
        if not role_id:
            return f"No role name matches for '{role_name}'. Please provide the correct role name."
        
        business_name = fetch_business_name_from_api(business, authorization_header)
        if not business_name:
            return f"Business name '{business}' does not exist."


        headers = {'Authorization': authorization_header, 'Content-Type': 'application/json'}
        payload = {
            "first_name": first_name,
            "last_name": last_name,
            "mobile_no": mobile_no,
            "email": email,
            "parent": parent_id,
            "role": role_id,
            "business": business_name,
            "designation": designation,
            "pan_no": pan_no,
            "aadhar_no": aadhar_no,
            "is_active": "true"
        }
        logging.info(f"Creating user with payload: {json.dumps(payload, indent=2)} and headers: {headers}")
        
        async with httpx.AsyncClient() as client:
            response = await client.post(f"https://{sso}/api/auth/register/", json=payload, headers=headers)
        
        logging.info(f"Response received with status code {response.status_code} and body {response.text}")
        
        response.raise_for_status()  # Raise an error for bad status codes
        if response.status_code == 200:
            return f"User '{first_name} {last_name}' created successfully."
        else:
            logging.info(f"Failed to create user. Response: {response.text}")
            return f"Failed to create user. Response: {response.text}"
    
    except httpx.HTTPStatusError as e:
        logging.info(f"HTTP error occurred: {e.response.status_code} - {e.response.text}")
        return f"Failed to create user. Error: {e.response.text}"
    
    except Exception as e:
        logging.error(f"An error occurred: {traceback.format_exc()}")
        return f"Failed to create user. Error: {str(e)}"

async def pause_user_tool(user_name, authorization_header, mobile_no=None):
    # import pdb; pdb.set_trace()
    try:
        user_id = None
        if user_name:
            users = fetch_user_id_from_name(user_name, authorization_header)
            if len(users) == 0:
                return f"No user found with the name '{user_name}'."
            elif len(users) == 1:
                user_id = users[0]['id']
            else:
                if not mobile_no:
                    return f"Multiple users found with the name '{user_name}'. Please provide a mobile number."
                matched_user = next((user for user in users if user['mobile_no'] == mobile_no), None)
                if matched_user:
                    user_id = matched_user['id']
                else:
                    return f"No user found with the name '{user_name}' and mobile number '{mobile_no}'."
        elif mobile_no:
            user_id = fetch_user_id_from_mobile_no(mobile_no, authorization_header)

        if user_id:
            headers = {'Authorization': authorization_header, 'Content-Type': 'application/x-www-form-urlencoded'}
            payload = {
                "is_active": "false",
                "collections": "[]"
            }
            logging.info(f"Pausing user with ID {user_id} with payload: {json.dumps(payload, indent=2)} and headers: {headers}")
            
            async with httpx.AsyncClient() as client:
                response = await client.put(f"https://{sso}/api/auth/register/{user_id}/", data=payload, headers=headers)
            logging.info(f"Response received with status code {response.status_code} and body {response.text}")
            response.raise_for_status()
            if response.status_code == 200:
                return f"User with Name '{user_name}' paused."
            else:
                logging.info(f"Failed to pause user. Response: {response.text}")
                return f"Failed to pause user. Response: {response.text}"
        else:
            return f"Failed to fetch user ID for name '{user_name}' or mobile number '{mobile_no}'. User not found."
    except httpx.HTTPStatusError as e:
        logging.info(f"HTTP error occurred: {e.response.status_code} - {e.response.text}")
        return f"Failed to pause user. Error: {e.response.text}"
    except Exception as e:
        logging.error(f"An error occurred: {traceback.format_exc()}")
        return f"Failed to pause user. Error: {str(e)}"

async def unpause_user_tool(user_name, authorization_header, mobile_no=None):
    # import pdb; pdb.set_trace()
    try:
        user_id = None

        if user_name:
            users = fetch_user_id_from_name(user_name, authorization_header)
            if len(users) == 0:
                return f"No user found with the name '{user_name}'."
            elif len(users) == 1:
                user_id = users[0]['id']
            else:
                if not mobile_no:
                    return f"Multiple users found with the name '{user_name}'. Please provide a mobile number."
                matched_user = next((user for user in users if user['mobile_no'] == mobile_no), None)
                if matched_user:
                    user_id = matched_user['id']
                else:
                    return f"No user found with the name '{user_name}' and mobile number '{mobile_no}'."
        elif mobile_no:
            user_id = fetch_user_id_from_mobile_no(mobile_no, authorization_header)

        if user_id:
            headers = {'Authorization': authorization_header, 'Content-Type': 'application/x-www-form-urlencoded'}
            payload = {
                "is_active": "true",
                "collections": "[]"
            }
            logging.info(f"Unpausing user with ID {user_id} with payload: {json.dumps(payload, indent=2)} and headers: {headers}")
            
            async with httpx.AsyncClient() as client:
                response = await client.put(f"https://{sso}/api/auth/register/{user_id}/", data=payload, headers=headers)
            logging.info(f"Response received with status code {response.status_code} and body {response.text}")
            response.raise_for_status()
            if response.status_code == 200:
                return f"User with name '{user_name}' unpaused."
            else:
                logging.info(f"Failed to unpause user. Response: {response.text}")
                return f"Failed to unpause user. Response: {response.text}"
        else:
            return f"Failed to fetch user ID for name '{user_name}' or mobile number '{mobile_no}'. User not found."
    except httpx.HTTPStatusError as e:
        logging.info(f"HTTP error occurred: {e.response.status_code} - {e.response.text}")
        return f"Failed to unpause user. Error: {e.response.text}"
    except Exception as e:
        logging.info(f"An error occurred: {traceback.format_exc()}")
        return f"Failed to unpause user. Error: {str(e)}"

async def assign_project_tool(user_name, project_name, authorization_header):
    try:
        project_ids = get_project_ids(user_name, project_name, authorization_header)

        headers = {'Authorization': authorization_header, 'Content-Type': 'application/json'}

        if not project_ids:  # No projects found, assign the project
            user_id = fetch_user_id_from_api(user_name, authorization_header)
            if not user_id:
                return "Failed to fetch user ID."
            project_name, parent_doc_id = get_project_parent_id(project_name, authorization_header)
            if not parent_doc_id:
                return "Failed to fetch project parent document ID."

            payload = {
                "parent_doc_id": parent_doc_id,
                "user_id": str(user_id),
                "project": project_name,
                "count": "0"
            }
            logging.info(f"Assigning project with payload: {json.dumps(payload, indent=2)} and headers: {headers}")
            async with httpx.AsyncClient() as client:
                response = await client.post(f"https://{dynamicurls}/projectassignment/create", json=payload, headers=headers)
            logging.info(f"Response received with status code {response.status_code} and body {response.text}")
            response.raise_for_status()  # Raise an error for bad status codes
            if response.status_code == 200:
                return f"User '{user_name}' assigned to project '{project_name}'."
            else:
                logging.error(f"Failed to assign project. Response: {response.text}")
                return f"Failed to assign project. Response: {response.text}"
        else:  # Projects found, reassign the project
            for project_id in project_ids:
                params = {
                    "id": project_id,
                    "key": "active",
                    "value": "true"  # Change the value to true to reassign (activate) the project
                }
                logging.info(f"Reassigning project with params: {json.dumps(params, indent=2)} and headers: {headers}")
                async with httpx.AsyncClient() as client:
                    response = await client.get(f"https://{dynamicurls}/projectassignment/PartialUpdate", params=params, headers=headers)
                logging.info(f"Response received with status code {response.status_code} and body {response.text}")
                response.raise_for_status()  # Raise an error for bad status codes
                if response.status_code == 201:
                    logging.info(f"Project with ID '{project_id}' reassigned.")
                else:
                    logging.error(f"Failed to reassign project. Response: {response.text}")
                    return f"Failed to reassign project. Response: {response.text}"

            return f"Projects reassigned for user: {user_name} with project name: {project_name}."
    except httpx.HTTPStatusError as e:
        logging.error(f"HTTP error occurred: {e.response.status_code} - {e.response.text}")
        return f"Failed to assign or reassign project. Error: {e.response.text}"
    except Exception as e:
        logging.error(f"An error occurred: {traceback.format_exc()}")
        return f"Failed to assign or reassign project. Error: {str(e)}"


async def unassign_project_tool(user_name, project_name, authorization_header):
    try:
        # Fetch project IDs for the user and project name
        project_ids = get_project_ids(user_name, project_name, authorization_header)
        if not project_ids:
            return f"No projects found for user ID: {user_name} and project name: {project_name}."

        # Unassign projects
        for project_id in project_ids:
            headers = {'Authorization': authorization_header, 'Content-Type': 'application/json'}
            params = {
                "id": project_id,
                "key": "active",
                "value": "false"
            }
            logging.info(f"Unassigning project with params: {json.dumps(params, indent=2)} and headers: {headers}")
            # import pdb; pdb.set_trace()
            async with httpx.AsyncClient() as client:
                response = await client.get(f"https://{dynamicurls}/projectassignment/PartialUpdate", params=params, headers=headers)
            logging.info(f"Response received with status code {response.status_code} and body {response.text}")
            response.raise_for_status()  # Raise an error for bad status codes
            if response.status_code == 201:
                logging.info(f"Project with ID '{project_id}' unassigned.")
            else:
                logging.info(f"Failed to unassign project. Response: {response.text}")
        return f"Projects unassigned for user: {user_name} with project name: {project_name}."
    except httpx.HTTPStatusError as e:
        logging.info(f"HTTP error occurred: {e.response.status_code} - {e.response.text}")
        return f"Failed to unassign project. Error: {e.response.text}"
    except Exception as e:
        logging.error(f"An error occurred: {traceback.format_exc()}")
        return f"Failed to unassign project. Error: {str(e)}"


async def user_info_query_tool(user_name, authorization_header, info_type):
    api_url = f"https://{sso}/api/user/"
    headers = {
        'Authorization': authorization_header,
        'Content-Type': 'application/json'
    }
    logging.info(f"Fetching user info from {api_url}")

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(api_url, headers=headers) as response:
                response.raise_for_status()
                data = await response.json()
                data = data.get('result', [])

        normalized_user_name = user_name.lower().strip()
        user_name_parts = normalized_user_name.split()

        if len(user_name_parts) < 1:
            logging.error("User name must contain at least a first name.")
            return f"Invalid user name: {user_name}"

        first_name = user_name_parts[0]
        last_name = user_name_parts[1] if len(user_name_parts) > 1 else None

        potential_matches = []

        for user in data:
            user_first_name = user['first_name'].lower()
            user_last_name = user['last_name'].lower() if user['last_name'] else ''

            full_name = f"{user['first_name']} {user['last_name']}".lower()
            if full_name == normalized_user_name:
                return await format_user_info(user, info_type)

            if first_name == user_first_name:
                potential_matches.append(user)

        if last_name:
            for user in potential_matches:
                if user['last_name'] and user['last_name'].lower() == last_name:
                    return await format_user_info(user, info_type)
        else:
            if len(potential_matches) == 1:
                return await format_user_info(potential_matches[0], info_type)
            elif len(potential_matches) > 1:
                logging.error("Multiple users with the same first name found. Please provide the last name.")
                return f"Multiple users with the same first name found. Please provide the last name."
            else:
                full_names = [f"{user['first_name']} {user['last_name']}".lower() for user in data]
                closest_match = difflib.get_close_matches(normalized_user_name, full_names, n=1, cutoff=0.6)

                if closest_match:
                    for user in data:
                        if f"{user['first_name']} {user['last_name']}".lower() == closest_match[0]:
                            return await format_user_info(user, info_type)

                logging.info("No close match found for the user name")
                return f"No match found for the user name: {user_name}"

    except aiohttp.ClientResponseError as e:
        logging.error("Failed to fetch users from the API: %s", e)
        logging.error(traceback.format_exc())
        return f"Failed to fetch user information. Error: {str(e)}"
    except Exception as e:
        logging.error(f"An error occurred: {traceback.format_exc()}")
        return f"Failed to fetch user information. Error: {str(e)}"

async def format_user_info(user, info_type):
    if info_type == "status":
        user_status = "active" if user.get('is_active') else "inactive"
        return f"The user {user['first_name']} {user['last_name']} is currently {user_status}."
    elif info_type == "count":
        return f"There is 1 user with the name {user['first_name']} {user['last_name']}."
    elif info_type == "mobile_number":
        return f"The mobile number of the user {user['first_name']} {user['last_name']} is {user.get('mobile_no', 'not available')}."
    elif info_type == "pan_number":
        return f"The PAN number of the user {user['first_name']} {user['last_name']} is {user.get('pan_no', 'not available')}."
    elif info_type == "aadhaar_number":
        return f"The Aadhaar number of the user {user['first_name']} {user['last_name']} is {user.get('aadhar_no', 'not available')}."
    elif info_type == "email":
        return f"The Aadhaar number of the user {user['first_name']} {user['last_name']} is {user.get('email', 'not available')}."
    else:
        user_status = "active" if user.get('is_active') else "inactive"
        return F"{user['first_name']} {user['last_name']} status: {user_status}\n mobile number: {user.get('mobile_no', 'not available')}\n Email: {user.get('email', 'not available')}\n PAN number: {user.get('pan_no', 'not available')} \n Aadhar Number: {user.get('aadhar_no', 'not available')}"
    

async def fetch_lists_tool(list_type, authorization_header):
    async def fetch_roles():
        api_url = f"https://{sso}/api/roles/"
        headers = {
            'Authorization': authorization_header,
            'Content-Type': 'application/json'
        }
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(api_url, headers=headers) as response:
                    response.raise_for_status()
                    data = await response.json()
                    return json.dumps([role['name'] for role in data.get('result', [])])
        except aiohttp.ClientError as e:
            logging.error("Failed to fetch roles from the API: %s", e)
            logging.error(traceback.format_exc())
            return json.dumps([])

    async def fetch_team_leaders():
        api_url = f"https://{sso}/api/user"
        headers = {
            'Authorization': authorization_header,
            'Content-Type': 'application/json'
        }
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(api_url, headers=headers) as response:
                    response.raise_for_status()
                    data = await response.json()
                    return json.dumps([f"{user['first_name']} {user['last_name']}" for user in data.get('result', []) if user['first_name'] and user['last_name']])
        except aiohttp.ClientError as e:
            logging.error("Failed to fetch users from the API: %s", e)
            logging.error(traceback.format_exc())
            return json.dumps([])

    async def fetch_businesses():
        # url = "https://crud-admindev.evoluxar.com/api/business/"
        url = f"https://{crudurl}/api/business/"
        headers = {
            'Authorization': authorization_header,
            'Content-Type': 'application/json'
        }
        logging.info(f"Fetching from URL: {url}")
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url, headers=headers) as response:
                    response.raise_for_status()
                    data = await response.json()
                    return json.dumps([business['name'] for business in data.get('result', [])])
        except aiohttp.ClientError as e:
            logging.error("Failed to fetch businesses from the API: %s", e)
            logging.error(traceback.format_exc())
            return json.dumps([])

    if list_type == "roles":
        return await fetch_roles()
    elif list_type == "team_leaders":
        return await fetch_team_leaders()
    elif list_type == "businesses":
        return await fetch_businesses()
    else:
        return json.dumps({"error": "Invalid list type specified"})

def get_date_time():
    try:
        response = requests.get('http://worldtimeapi.org/api/ip')  # Fetches time from an internet time server
        if response.status_code == 200:
            data = response.json()
            datetime_str = data['datetime']
            datetime_obj = datetime.strptime(datetime_str, '%Y-%m-%dT%H:%M:%S.%f%z')  # Parse the datetime string
            return datetime_str
        else:
            return 'Failed to fetch date and time'
    except requests.RequestException as e:
        return 'Failed to fetch date and time'

async def get_perforance_tool(token,start_date,end_date,user_name):
    #
    # Get the access token
    print(start_date,end_date,user_name)
    bearer_token = token
    print("barri",bearer_token)
    headers = {
        "Authorization": bearer_token,
        "Content-Type": "application/json"
    }
    print(headers)
    user_id = fetch_user_id_from_api(user_name, bearer_token)
    per=[]
    if user_id:
        url = f"https://{urls}/team-member-performance/lead-source?start_date={start_date}&end_date={end_date}&user_list={user_id}"

        async with httpx.AsyncClient(timeout=None) as client:
            response = await client.get(url, headers=headers)

            if response.status_code == 200:
                lead_source = f"this is the lead source: {response.json()}"
                per.append(lead_source)
                
            else:
                lead_source = f"the lead source data api is not working"
                per.append(lead_source)
        url2 = f"https://{urls}/team-member-performance/comparative-analysis?start_date={start_date}&end_date={end_date}&user_list={user_id}"

        async with httpx.AsyncClient(timeout=None) as client:
            response = await client.get(url2, headers=headers)

            if response.status_code == 200:
                lead_source = f"this is the comparative-analysis: {response.json()}"
                per.append(lead_source)    
            else:
                lead_source = f"the comparative-analysis api is not working"
                per.append(lead_source)
        url3 = f"https://{urls}/team-member-performance/productivity?start_date={start_date}&end_date={end_date}&user_list={user_id}&timeframe="

        async with httpx.AsyncClient(timeout=None) as client:
            response = await client.get(url3, headers=headers)

            if response.status_code == 200:
                lead_source = f"this is the comparative-analysis: {response.json()}"
                per.append(lead_source)    
            else:
                lead_source = f"the comparative-analysis api is not working"
                per.append(lead_source)  
        print(str(per)) 
        return str(per)   
    return str("no user found for this name")                       
