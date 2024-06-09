create_user = {
    "name": "Create_User",
    "description": "Use this function to create a new user in the system.",
    "parameters": {
        "type": "object",
        "properties": {
            "first_name": {"type": "string", "description": "The first name of the user to be created."},
            "last_name": {"type": "string", "description": "The last name of the user to be created."},
            "mobile_no": {"type": "string", "description": "The mobile number of the user to be created."},
            "email": {"type": "string", "description": "The email ID of the user to be created."},
            "parent_name": {"type": "string", "description": "The parent name or head name of the user."}, 
            "role_name": {"type": "string", "description": "The role name of the user to be assigned."},
            "business": {"type": "string", "description": "The business associated with the user."},
        },
        "required": ["first_name", "last_name","mobile_no", "email", "parent_name", "role_name", "business"]
    }
}


pause_user = {
    "name": "Pause_User",
    "description": "Use this function to pause or deactivate a user in the system.",
    "parameters": {
        "type": "object",
        "properties": {
            "user_name": {"type": "string", "description": "The name of the user to be paused."},
            "mobile_no": {
                "type": "string", 
                "description": "The mobile number of the user to be paused (required if multiple users with the same name exist).",
                "format": "mobile-number"
                }
        },
        "required": ["user_name"],
        "optional": ["mobile_no"]
    }
}

unpause_user = {
    "name": "Unpause_User",
    "description": "Use this function to unpause or activate a user in the system.",
    "parameters": {
        "type": "object",
        "properties": {
            "user_name": {"type": "string", "description": "The name of the user to be unpaused."},
            "mobile_no": {
                "type": "string", 
                "description": "The mobile number of the user to be unpaused (required if multiple users with the same name exist).",
                "format": "mobile-number"
                }
        },
        "required": ["user_name"],
        "optional": ["mobile_no"]
    }
}


assign_project = {
    "name": "Assign_Project",
    "description": "Use this function to assign a user to a project.",
    "parameters": {
        "type": "object",
        "properties": {
            "user_name": {"type": "string", "description": "The full name of the user to be assigned."},
            "project_name": {"type": "string", "description": "The name of the project to be assigned."}
        },
        "required": ["user_name", "project_name"]
    }
}


unassign_project = {
    "name": "Unassign_Project",
    "description": "Use this function to unassign a project from a user.",
    "parameters": {
        "type": "object",
        "properties": {
            "user_name": {"type": "string", "description": "The full name of the user from whom the project is to be unassigned."},
            "project_name": {"type": "string", "description": "The name of the project to be unassigned."}
        },
        "required": ["user_name", "project_name"]
    }
}
