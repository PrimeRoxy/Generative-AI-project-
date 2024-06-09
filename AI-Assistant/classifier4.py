import json
import os
import openai 
from classifier07 import generate_parameters

prompt_template = """
Context: You are building a system that requires gathering specific input parameters from users based on required input parameters. The system should prompt users for input, validate it, and ensure all required parameters are provided. Your task is to generate a message template to guide this interaction one by one for input there will be a placeholder.

Instructions:
1. Based on the required input parameters.
2. Generate a message to prompt the user for their input.
3. Ensure the generated message includes placeholders for each required parameter.
4. Once the user provides input, validate it and check if any required parameters are missing.
5. If any parameters are missing, prompt the user for the missing input.

Your message template should follow this structure:
- Begin by acknowledging the user query.
- Prompt the user for input based on the identified parameters. Ensure the generated message includes placeholders for each required parameter.

Message Template:
Please enter your query: {user_query}
{parameter_prompts}

"""

client = openai.OpenAI()
openai.api_key = os.getenv('OPENAI_API_KEY')
action_detail_file = "action_details.json"

def process_user_input(action_detail_file, user_query):
    required_parameters = generate_parameters(action_detail_file, user_query)
    if not required_parameters:
        return None

    try:
        with open(action_detail_file, 'r') as file:
            data = json.load(file)
    except FileNotFoundError:
        print("Action details file not found.")
        return None

    build_response = client.chat.completions.create(
        model='gpt-4',
        messages=[
            {"role": "system", "content": prompt_template},
            {"role": "user", "content": f"Please provide input for the following parameters: \"{required_parameters}\". We are awaiting your response."}   
        ],
        temperature=0,
    )

    messages = build_response.choices[0].message.content.strip().split('\n')
    # Create a dictionary to store user input data
    user_data = {}

    for message in messages[1:]:
       if any(char.isdigit() for char in message.strip()) and '.' in message.strip():
        # Prompt the user to enter input for the current parameter
            user_input = input(f"{message.strip()}: ")

            # Store user input in user_data dictionary
            parameter, value = message.strip().split(':', 1)
            user_data[parameter.strip()] = user_input

        # Print user_data dictionary
    # print("User input data:")
    # print(json.dumps(user_data, indent=4))
    return user_data

def main():
    while True:
        user_query = input("Please enter your query: ")
        process_user_input(action_detail_file,user_query)
        if user_query.lower() == "exit":
            print("Exiting...")
            break

if __name__ == "__main__":
    main() 