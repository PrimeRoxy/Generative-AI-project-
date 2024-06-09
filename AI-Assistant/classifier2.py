# Discover Action_id based on user query

import os
import json
import openai
from classifier1 import classify_message_with_gpt4

# Set your OpenAI API key
openai.api_key = os.getenv('OPENAI_API_KEY')
client = openai.OpenAI()

action_prompt = """
Prompt: You are a helpful assistant. You role is to analyze the user query and find best matching action to the query from the list of actions provided to you in JSON format as below with key value pair of ActionID, Title and Description. You job is to ONLY return the ActionID of the action you think is appropriate based on user intent in query.
You need to strictly respond with ONLY action ID, nothing else. If there is no relevant action found, return “No Action Found”
"""

def discover_action_id(action_detail_file, user_query):

    classification, _ = classify_message_with_gpt4(user_query)

    if classification == "ACTION REQUEST":
        print(classification)
    else:
        print("User query is not an action request.")
        return None
    try:
        with open(action_detail_file, 'r') as file:
            data = json.load(file)
    except FileNotFoundError:
        print("Action details file not found.")
        return None

    search_text = data
    similarity_response = client.chat.completions.create(
        model='gpt-4',
        messages=[
            {"role": "system", "content": action_prompt},
            {"role": "user", "content": f"Similarity between \"{user_query}\" and \"{search_text}\""}   
        ],
        temperature=0,
    )

    similarity = similarity_response.choices[0].message.content.strip()
    return similarity

def main():
    action_detail_file = "action_details.json"
    while True:
        user_query = input("Please enter your query: ")
        if user_query.lower() == "exit":
            print("Exiting...")
            break

        best_match_id = discover_action_id(action_detail_file, user_query)
        if best_match_id:
            print("Action id:", best_match_id)
        else:
            print("No matching action found.")

if __name__ == "__main__":
    main() 

