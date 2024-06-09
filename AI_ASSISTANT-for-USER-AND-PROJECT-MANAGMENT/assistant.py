import asyncio
import json
import os
from openai import OpenAI
from dotenv import load_dotenv
from .assistant_functionality import create_user, pause_user, unpause_user, assign_project, unassign_project
from .user_management_tools import (
    create_user_tool, pause_user_tool, unpause_user_tool, assign_project_tool, unassign_project_tool
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
]

assistant_id = "YOUR ASSISTANT ID"

async def process_assistant_task(user_query, authorization_header):
    logging.info(f"Processing user query: {user_query}")
    
    try:
        thread = client.beta.threads.create()
        logging.info(f"Created new thread with ID: {thread.id}")

        client.beta.threads.messages.create(
            thread_id=thread.id,
            role="user",
            content=user_query
        )

        run = client.beta.threads.runs.create(
            thread_id=thread.id,
            assistant_id=assistant_id,
        )
        logging.info(f"Created new run in thread ID {thread.id} with assistant ID {assistant_id}")
    except Exception as e:
        logging.info(f"Error creating thread or run: {str(e)}")
        return {"detail": "Failed to create thread or run"}

    while True:
        try:
            await asyncio.sleep(5)

            run_status = client.beta.threads.runs.retrieve(
                thread_id=thread.id,
                run_id=run.id
            )
            

            if run_status.status == 'completed':
                messages = client.beta.threads.messages.list(
                    thread_id=thread.id
                )
                message_texts = [msg.content[0].text.value.strip() for msg in messages.data[:-1]]
                logging.info(f"Run completed. Messages: {message_texts}")

                return {"messages": message_texts}

            elif run_status.status == 'requires_action':
                required_actions = run_status.required_action.submit_tool_outputs.model_dump()
                logging.info(f"Run requires action: {required_actions}")

                tool_output_array = []
                for action in required_actions["tool_calls"]:
                    func_name = action['function']['name']
                    arguments = json.loads(action['function']['arguments'])
                    logging.info(f"Executing function {func_name} with arguments: {arguments}")

                    try:
                        if func_name == "Create_User":
                            output = await create_user_tool(
                                first_name=arguments['first_name'],
                                last_name=arguments['last_name'],
                                mobile_no=arguments['mobile_no'],
                                email=arguments['email'],
                                parent_name=arguments['parent_name'],
                                role_name=arguments['role_name'],
                                business=arguments['business'],
                                authorization_header=authorization_header
                            )

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

                        elif func_name == "Assign_Project":
                            output = await assign_project_tool(
                                user_name=arguments['user_name'],
                                project_name=arguments['project_name'],
                                authorization_header=authorization_header
                            )

                        elif func_name == "Unassign_Project":
                            output = await unassign_project_tool(
                                user_name=arguments['user_name'],
                                project_name=arguments['project_name'],
                                authorization_header=authorization_header
                            )
                        else:
                            raise ValueError(f"Unknown function: {func_name}")

                        logging.info(f"Function {func_name} executed successfully. Output: {output}")
                    except Exception as e:
                        logging.info(f"Error executing function {func_name}: {str(e)}")
                        output = f"Error executing function {func_name}: {str(e)}"

                    tool_output_array.append({
                        "tool_call_id": action['id'],
                        "output": output
                    })

                client.beta.threads.runs.submit_tool_outputs(
                    thread_id=thread.id,
                    run_id=run.id,
                    tool_outputs=tool_output_array
                )
                logging.info(f"Submitted tool outputs for run ID {run.id}")

            elif run_status.status == 'failed':
                logging.info(f"Run ID {run.id} failed.")
                return {"detail": "The assistant failed to process the request."}

            else:
                await asyncio.sleep(5)
        except Exception as e:
            logging.info(f"Error during run processing: {str(e)}")
            return {"detail": "An error occurred during processing"}

