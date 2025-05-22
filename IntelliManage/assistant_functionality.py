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
            "team_leader": {"type": "string", "description": "The team_leader name of the user."}, 
            "role_name": {"type": "string", "description": "The role name of the user to be assigned."},
            "business": {"type": "string", "description": "The business associated with the user."},
            "designation": {"type": "string", "description": "The user's job title or designation."},
            "pan_no": {"type": "string", "description": "The PAN number of the user (optional)."},
            "aadhar_no": {"type": "string", "description": "The Aadhar number of the user (optional)."},

        },
        "required": ["first_name", "last_name","mobile_no", "email", "team_leader", "role_name", "business", "designation"]
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

user_info_query = {
    "name": "User_Info_Query",
    "description": "Use this function to retrieve various details about a user.",
    "parameters": {
        "type": "object",
        "properties": {
            "user_name": {"type": "string", "description": "The full name of the user."},
            "info_type": {"type": "string", "description": "The type of information requested (status, count, mobile_number, pan_number, aadhaar_number)."}
        },
        "required": ["user_name", "info_type"]
    }
}

fetch_lists = {
    "name": "Fetch_Lists",
    "description": "Use this function to fetch lists of businesses, roles, and team leaders.",
    "parameters": {
        "type": "object",
        "properties": {
            "list_type": {
                "type": "string",
                "description": "The type of list to fetch. Must be one of 'roles', 'team_leaders', or 'businesses'."
            }
        },
        "required": ["list_type"]
    }
}
dt_tm = {
	"name" : "dt_tm",
	"description" : "Use this function to get current time and date .",
	"parameters" : {

		"type" : "object",
		"properties" : {
			"name" : {
				"type" : "string",
				"description" : "The name of user to get time date for"
				}
		},
	"required" : []
}}

user_performance = {
  "name": "user_performance",
  "description": "Use this function to find the answer of performance, comparative-analysis, productivity of specific user/team related questions.always Use dt_tm tool for current date and time. If in the question, mention today, yesterday, May, this month, or this year, convert it into YYYY-MM-DD format. If the fields end_date and start_date are not in the question, end_date is equal to the current date, and start_date is equal to one month before the current date.",
  #"strict": false,
  "parameters": {
    "type": "object",
    "properties": {
      "start_date": {
        "type": "string",
        "description": "Find the start date if mentioned in the question. Date format is YYYY-MM-DD. This field is always required."
      },
      "end_date": {
        "type": "string",
        "description": "Find the end date if mentioned in the question. Date format is YYYY-MM-DD. This field is always required."
      },
      "user_name": {
        "type": "string",
        "description": "This is name of the user/team ."
      }
    },
    "required": [
      "start_date",
      "end_date",
      "user_name"
    ]
  }
}