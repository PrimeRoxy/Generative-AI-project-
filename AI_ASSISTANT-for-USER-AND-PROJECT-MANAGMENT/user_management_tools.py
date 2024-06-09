import os
from dotenv import load_dotenv
import httpx
import json
import logging
from .helper import fetch_parent_id_from_api, fetch_role_id_from_api, fetch_user_id_from_api, fetch_user_id_from_mobile_no, fetch_user_id_from_name, get_project_ids, get_project_parent_id
load_dotenv()

API_BASE_URL_AUTH = os.getenv("api_base_url_auth")
API_BASE_URL_PROJECT = os.getenv("api_base_url_project")

# Configure logging
logging.basicConfig(level=logging.INFO)

async def create_user_tool(first_name, last_name, mobile_no, email, parent_name, role_name, business, authorization_header):
    try:
        parent_id = fetch_parent_id_from_api(parent_name, authorization_header)
        if not parent_id:
            return f"Failed to fetch parent ID for parent name '{parent_name}'"

        role_id = fetch_role_id_from_api(role_name, authorization_header)
        if not role_id:
            return f"Failed to fetch role ID for role name '{role_name}'"

        headers = {'Authorization': authorization_header, 'Content-Type': 'application/json'}
        payload = {
            "first_name": first_name,
            "last_name": last_name,
            "mobile_no": mobile_no,
            "email": email,
            "parent": parent_id,
            "role": role_id,
            "business": business
        }
        logging.info(f"Creating user with payload: {json.dumps(payload, indent=2)} and headers: {headers}")
        
        async with httpx.AsyncClient() as client:
            response = await client.post(f"https://{API_BASE_URL_AUTH}/register/", json=payload, headers=headers)
        
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
        logging.info(f"An error occurred: {e}")
        return f"Failed to create user. Error: {str(e)}"

async def pause_user_tool(user_name, authorization_header, mobile_no=None):
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
                response = await client.put(f"https://{API_BASE_URL_AUTH}/register/{user_id}/", data=payload, headers=headers)
            logging.info(f"Response received with status code {response.status_code} and body {response.text}")
            response.raise_for_status()
            if response.status_code == 200:
                return f"User with ID '{user_id}' paused."
            else:
                logging.info(f"Failed to pause user. Response: {response.text}")
                return f"Failed to pause user. Response: {response.text}"
        else:
            return f"Failed to fetch user ID for name '{user_name}' or mobile number '{mobile_no}'. User not found."
    except httpx.HTTPStatusError as e:
        logging.info(f"HTTP error occurred: {e.response.status_code} - {e.response.text}")
        return f"Failed to pause user. Error: {e.response.text}"
    except Exception as e:
        logging.info(f"An error occurred: {e}")
        return f"Failed to pause user. Error: {str(e)}"

async def unpause_user_tool(user_name, authorization_header, mobile_no=None):
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
                response = await client.put(f"https://{API_BASE_URL_AUTH}/register/{user_id}/", data=payload, headers=headers)
            logging.info(f"Response received with status code {response.status_code} and body {response.text}")
            response.raise_for_status()
            if response.status_code == 200:
                return f"User with ID '{user_id}' unpaused."
            else:
                logging.info(f"Failed to unpause user. Response: {response.text}")
                return f"Failed to unpause user. Response: {response.text}"
        else:
            return f"Failed to fetch user ID for name '{user_name}' or mobile number '{mobile_no}'. User not found."
    except httpx.HTTPStatusError as e:
        logging.info(f"HTTP error occurred: {e.response.status_code} - {e.response.text}")
        return f"Failed to unpause user. Error: {e.response.text}"
    except Exception as e:
        logging.info(f"An error occurred: {e}")
        return f"Failed to unpause user. Error: {str(e)}"

async def assign_project_tool(user_name, project_name, authorization_header):
    try:
        user_id = fetch_user_id_from_api(user_name, authorization_header)
        if not user_id:
            return "Failed to fetch user ID."

        project_name, parent_doc_id = get_project_parent_id(project_name, authorization_header)
        if not parent_doc_id:
            return "Failed to fetch project parent document ID."

        headers = {'Authorization': authorization_header, 'Content-Type': 'application/json'}
        payload = {
            "parent_doc_id": parent_doc_id,
            "user_id": str(user_id),
            "project": project_name,
            "count": "0"
        }
        logging.info(f"Assigning project with payload: {json.dumps(payload, indent=2)} and headers: {headers}")
        async with httpx.AsyncClient() as client:
            response = await client.post(f"https://{API_BASE_URL_PROJECT}/create", json=payload, headers=headers)
        logging.info(f"Response received with status code {response.status_code} and body {response.text}")
        response.raise_for_status()  # Raise an error for bad status codes
        if response.status_code == 200:
            return f"User '{user_name}' assigned to project '{project_name}'."
        else:
            logging.info(f"Failed to assign project. Response: {response.text}")
            return f"Failed to assign project. Response: {response.text}"
    except httpx.HTTPStatusError as e:
        logging.info(f"HTTP error occurred: {e.response.status_code} - {e.response.text}")
        return f"Failed to assign project. Error: {e.response.text}"
    except Exception as e:
        logging.info(f"An error occurred: {e}")
        return f"Failed to assign project. Error: {str(e)}"

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
            async with httpx.AsyncClient() as client:
                response = await client.get(f"https://{API_BASE_URL_PROJECT}/PartialUpdate", params=params, headers=headers)
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
        logging.info(f"An error occurred: {e}")
        return f"Failed to unassign project. Error: {str(e)}"
