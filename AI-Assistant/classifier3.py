import json
import os
import openai 
from classifier6 import discover_action_id

build_parameter_prompt = """
Prompt:
Build input parameters based on the provided action ID.
find the input required from the user for taking that action

Action ID: [ACTION_ID]

Description:
The AI needs to know what inputs are needed in order to perform an action with a given Action ID.
Please provide the necessary input parameters. Ensure that all required fields are included and that the values are appropriate for the task.

"""

client = openai.OpenAI()
openai.api_key = os.getenv('OPENAI_API_KEY')
def generate_parameters(action_detail_file, user_query):
    action_id = discover_action_id(action_detail_file, user_query)
    if not action_id:
        return None
    try:
        with open(action_detail_file, 'r') as file:
            data = json.load(file)
    except FileNotFoundError:
        print("Action details file not found.")
        return None

    search_text = data
    build_response = client.chat.completions.create(
        model='gpt-4',
        messages=[
            {"role": "system", "content": build_parameter_prompt},
            {"role": "user", "content": f"Build parameter based on \"{action_id}\" and using \"{search_text}\""}   
        ],
        temperature=0,
    )

    build_IP = build_response.choices[0].message.content.strip()
    return build_IP

    
def main():
    while True:
        action_detail_file = "action_details.json"
        user_query = input("Please enter your query: ")
        ip = generate_parameters(action_detail_file, user_query)
        print(ip)
        if user_query.lower() == "exit":
            print("Exiting...")
            break

if __name__ == "__main__":
    main() 

