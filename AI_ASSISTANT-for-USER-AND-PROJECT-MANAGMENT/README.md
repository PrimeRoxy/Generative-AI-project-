# AI_ASSISTANT-for-USER-AND-PROJECT-MANAGMENT

This project processes user queries by interacting with an assistant, verifying authentication, and performing various user management functions. The assistant processes tasks like creating users, pausing/unpausing users, and assigning/unassigning projects.

## Table of Contents
- [Installation](#installation)
- [Usage](#usage)
- [Endpoints](#endpoints)
- [Code structure](#code_structure)



2. **Create a virtual environment**:
    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install the dependencies**:
    ```sh
    pip install -r requirements.txt
    ```

4. **Set up environment variables**:
    Create a `.env` file in the root directory of the project and add the following:
    ```
    ORGANIZATION=<your-organization>
    OPENAI_KEY=<your-openai-key>
    ```

## Usage

### Running the Application

1. **Start the FastAPI application**:
    ```sh
    uvicorn manage:app --reload
    ```


## Endpoints

### `POST /manage/`

- **Description**: Processes a user query.
- **Request Body**: 
    ```json
    {
        "user_query": "<Your user query>"
    }
    ```
- **Response**: 
    - `200 OK`: Successfully processed the query.
    - `401 Unauthorized`: Authentication failed.
    - `500 Internal Server Error`: Processing failed.


## Code Structure

### `manage.py`

This file initializes the FastAPI application and defines the `/manage/` endpoint, which processes user queries.


### `helper.py`

This file contains the `verify_authentication` function, which checks the validity of the `Authorization` header.
AND
This file includes functions for fetching user, role, and project details from the API based on different criteria.

### `assistant.py`

This file processes the user query using the OpenAI assistant and handles various user management tasks by interacting with predefined tools.

### `assistant_functionality.py`

Contains the Openai function for user management tasks such as `create_user`, `pause_user`, `unpause_user`, `assign_project`, and `unassign_project`.

### `user_management_tools.py`

Defines the tool functions that interact with the API to manage users and projects. It contains tools such as `create_user_tool`, `pause_user_tool`, `unpause_user_tool`, `assign_project_tool`, and `unassign_project_tool`.



### `Security Considerations`
Environment Variables: Keep sensitive information like API keys and server URLs secure. Use environment variables and never hard-code them into the source code.
Authentication: Ensure all endpoints are secured with proper authentication mechanisms.
Error Handling: Do not expose sensitive error information to end-users. Log detailed error information for internal review and debugging.


## License

This project is licensed under the MIT License. See the `LICENSE` file for details.

## Contact

For any questions or suggestions, please contact [vipuldashingboy@gmail.com](mailto:vipuldashingboy@gmail.com).