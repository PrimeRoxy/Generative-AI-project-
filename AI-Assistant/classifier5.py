import json
import os
import openai
import streamlit as st
from classifier8 import process_user_input

prompt_template = """
Prompt: You are entrusted with gracefully formatting data into JSON upon receiving input, which will then be utilized to invoke an API for executing a designated action. Your task involves crafting the JSON representation, initiating the API call, executing the specified action based on user input, and elegantly presenting the outcome.
"""

openai.api_key = os.getenv('OPENAI_API_KEY')
client = openai.OpenAI()

action_detail_file = "action_details.json"


def process_user_output(user_query):
    user_data = process_user_input(action_detail_file, user_query)
    if not user_data:
        return "No user data processed."
    
    try:
        with open(action_detail_file, 'r') as file:
            data = json.load(file)
    except FileNotFoundError:
        return "Action details file not found."
    
    output_response = client.chat.completions.create(
        model='gpt-4',
        messages=[
            {"role": "system", "content": prompt_template},
            {"role": "user", "content": f"\"{user_data}\" and use this data for response \"{data}\""}
        ],
        temperature=0,
    )
    
    response = output_response.choices[0].message.content.strip()
    return response


def main():
    st.title("AI-Powered Action Executor")
    
    user_query = st.text_input("Please enter your query:")
    
    if st.button("Process"):
        if user_query:
            response = process_user_output(user_query)
            st.write("Response:")
            st.json(response)
        else:
            st.write("Please enter a query to process.")
    
    if st.button("Exit"):
        st.write("Exiting...")

if __name__ == "__main__":
    main()
