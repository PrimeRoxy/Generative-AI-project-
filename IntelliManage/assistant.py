import asyncio
import json
import os
import traceback
from openai import OpenAI
from dotenv import load_dotenv
from .assistant_functionality import create_user, pause_user, unpause_user, assign_project, unassign_project,user_info_query,fetch_lists
from .user_management_tools import (
    create_user_tool, get_perforance_tool, pause_user_tool, unpause_user_tool, assign_project_tool, unassign_project_tool,user_info_query_tool,fetch_lists_tool,get_date_time
)
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)

load_dotenv()

# Initialize the OpenAI client
client = OpenAI(
    organization=os.getenv("organization"),
    api_key=os.getenv("openai_key"),
)

tools_list = [
    {"type": "function", "function": create_user},
    {"type": "function", "function": pause_user},
    {"type": "function", "function": unpause_user},
    {"type": "function", "function": assign_project},
    {"type": "function", "function": unassign_project},
    {"type": "function", "function": user_info_query},
    {"type": "function", "function": fetch_lists},

]

# assistant_id = "asst_aLjyCKNhvaN6YlfPgPPIpTIh" # this format 
assistant_id = "Your Assistant ID" 

user_data = {}
async def handle_missing_fields(arguments, thread_id):
    required_fields = ["first_name", "last_name", "mobile_no", "email", "team_leader", "role_name", "business", "designation"]
    optional_fields = ["pan_no", "aadhar_no"]
    missing_fields = [field for field in required_fields if field not in arguments or not arguments[field]]
    
    for field in missing_fields:
        response = client.beta.threads.messages.create(
            thread_id=thread_id,
            assistant_id=assistant_id,
            content=f"Please provide {field.replace('_', ' ')}: . Here role_name will be for the user in the system. user must have provided earlier in conversation please either use that or ask user to enter it again. please choose that."

        )
        await asyncio.sleep(5)  # Wait for the user to respond
        
        messages = client.beta.threads.messages.list(thread_id=thread_id)
        logging.info(f"Response :{messages}")
        user_response = messages.data[-1].content[0].text.value.strip()
        logging.info(f"Response :{user_response}")

        arguments[field] = user_response

        # Store the user response in user_data
        user_data[thread_id] = arguments

        # Add optional fields if provided
    for field in optional_fields:
        if field in arguments and arguments[field]:
            user_data[thread_id][field] = arguments[field]
    return arguments
    

async def process_assistant_task(user_query, authorization_header,thread_id):
    logging.info(f"Processing user query: {user_query}")
    
    try:

        client.beta.threads.messages.create(
            thread_id=thread_id,
            role="user",
            content=user_query
        )

        run = client.beta.threads.runs.create(
            thread_id=thread_id,
            assistant_id=assistant_id,
            additional_instructions = "Donot respond repetitive data or repetitive sentences. Be concise and precise. Always repond in one or two sentences only."
        )
        logging.info(f"thread ID {thread_id} with assistant ID {assistant_id}")
        logging.error(traceback.format_exc())
    except Exception as e:
        logging.info(f"Error creating  run: {str(e)}")
        logging.error(traceback.format_exc())
        return {"detail": "Failed to create run"}

    while True:
        try:
            await asyncio.sleep(5)

            run_status = client.beta.threads.runs.retrieve(
                thread_id=thread_id,
                run_id=run.id
            )
            

            if run_status.status == 'completed':
                messages = client.beta.threads.messages.list(
                    thread_id=thread_id
                )

                # Filter out user messages
                non_user_messages = [msg for msg in messages.data if msg.role != 'user']
    
                # Sort messages by timestamp in descending order to get the most recent one first
                non_user_messages.sort(key=lambda msg: msg.created_at, reverse=True)
                # Get the most recent response message
                recent_message = non_user_messages[0].content[0].text.value.strip() if non_user_messages else None

                logging.info(f"Run completed. Message: {recent_message}")
                return {"messages": recent_message}

            elif run_status.status == 'requires_action':
                required_actions = run_status.required_action.submit_tool_outputs.model_dump()
                logging.info(f"Run requires action: {required_actions}")

                tool_output_array = []
                for action in required_actions["tool_calls"]:
                    func_name = action['function']['name']
                    arguments = json.loads(action['function']['arguments'])
                    logging.info(f"Executing function {func_name} with arguments: {arguments}")
                    print(authorization_header)

                    try:
                        if func_name == "Create_User":
                             # Check for missing fields and request them if needed
                            if thread_id in user_data:
                                arguments.update(user_data[thread_id])
                            arguments = await handle_missing_fields(arguments, thread_id)
    
                            output = await create_user_tool(
                                first_name=arguments['first_name'],
                                last_name=arguments['last_name'],
                                mobile_no=arguments['mobile_no'],
                                email=arguments['email'],
                                team_leader=arguments['team_leader'],
                                role_name=arguments['role_name'],
                                business=arguments['business'],
                                designation=arguments['designation'],
                                pan_no=arguments.get('pan_no'),
                                aadhar_no=arguments.get('aadhar_no'),
                                authorization_header=authorization_header
                            )
                            # Clear user data after successful creation
                            if thread_id in user_data:
                                del user_data[thread_id]

                        elif func_name == "Pause_User":
                            user_name = arguments.get('user_name')
                            mobile_no = arguments.get('mobile_no')
                            output = await pause_user_tool(
                                user_name=user_name,
                                mobile_no=mobile_no,
                                authorization_header=authorization_header
                            )

                        elif func_name == "Unpause_User":
                            user_name = arguments.get('user_name')
                            mobile_no = arguments.get('mobile_no')
                            output = await unpause_user_tool(
                                user_name=user_name,
                                mobile_no=mobile_no,
                                authorization_header=authorization_header
                            )

                        elif func_name == "assign_project":
                            output = await assign_project_tool(
                                user_name=arguments['user_name'],
                                project_name=arguments['project_name'],
                                authorization_header=authorization_header
                            )

                        elif func_name == "unassign_project":
                            output = await unassign_project_tool(
                                user_name=arguments['user_name'],
                                project_name=arguments['project_name'],
                                authorization_header=authorization_header
                            )
                        
                        elif func_name == "User_Info_Query":
                            output = await user_info_query_tool(
                                user_name=arguments['user_name'],
                                info_type=arguments['info_type'],
                                authorization_header=authorization_header
                            )
                        elif func_name == 'dt_tm':
                            output = get_date_time()
                            print(output)
                        elif func_name == "user_performance":
                            output = await get_perforance_tool(
                                authorization_header,
                                arguments["start_date"],
                                arguments["end_date"],
                                arguments["user_name"]    
                            )
                            print(output)
                        
                        elif func_name == "Fetch_Lists":
                            output = await fetch_lists_tool(
                                list_type=arguments['list_type'],
                                authorization_header=authorization_header
                            )
                            # Properly format the response
                            list_data = json.loads(output)
                            response_message = f"The available {arguments['list_type'].replace('_', ' ')} in the system are: " + ", ".join(list_data)
                            output = json.dumps({"message": response_message})
                            logging.info(f"Function {func_name} executed successfully. Output: {output}")

                        else:
                            raise ValueError(f"Unknown function: {func_name}")

                        logging.info(f"Function {func_name} executed successfully. Output: {output}")
                    except Exception as e:
                        logging.error(f"Error executing function {func_name}: {str(e)}")
                        logging.error(traceback.format_exc())
                        output = f"Error executing function {func_name}: {str(e)}"

                    tool_output_array.append({
                        "tool_call_id": action['id'],
                        "output": output
                    })

                client.beta.threads.runs.submit_tool_outputs(
                    thread_id=thread_id,
                    run_id=run.id,
                    tool_outputs=tool_output_array
                )
                logging.info(f"Submitted tool outputs for run ID {run.id}")
                logging.error(traceback.format_exc())

            elif run_status.status == 'failed':
                logging.error(f"Run ID {run.id} failed.{traceback.format_exc()}")
                logging.error(traceback.format_exc())
                return {"detail": "The assistant failed to process the request."}

            else:
                await asyncio.sleep(5)
        except Exception as e:
            logging.error(f"Error during run processing: {str(e)}")
            logging.error(traceback.format_exc())
            return {"detail": "An error occurred during processing"}