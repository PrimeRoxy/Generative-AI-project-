# Custom category classifier

import os
import openai
from openai import OpenAI

# Constants for message categories
INFO_SHARED = "INFO SHARED"
ACTION_REQUEST = "ACTION REQUEST"
ASK = "ASK"
IMPLICIT_ACTION = "IMPLICIT ACTION"

# Define the prompt for message classification with explanations
classification_prompt = f"""
Prompt: Classify the message into one of the following categories: {INFO_SHARED}, {ACTION_REQUEST}, {ASK}, {IMPLICIT_ACTION}.

Message: "{{message}}"

Category: Based on the message, determine the category as one of the following:
- INFO SHARED: If the message provides information with no expected action.
- ACTION REQUEST: If the message instructs to perform an action.
- ASK: If the message is asking for some information.
- IMPLICIT ACTION: If the message shares information but implies a suggested action.

Explanation: Here are some tips to guide the classification:
- Look for keywords related to sharing information, performing actions, asking questions, or suggesting actions.
- Consider the context and tone of the message to determine the appropriate category.

For Explanation:
Prompt: Provide a detailed explanation of the message's intent, especially in the context of real estate transactions involving customers and agents.

Explanation: Please provide a detailed explanation for the message to help understand its purpose, considering it may involve real estate transactions between customers and agents. This could include context, background information, or any additional details that clarify the message's meaning in the real estate domain.


Example:
Message: "Please send the report by tomorrow."
Category: ACTION REQUEST
Explanation: The message instructs someone to send a report by tomorrow, indicating an urgent action is needed.

Message: "What time is the meeting?"
Category: ASK
Explanation: The message is asking for the time of a meeting, indicating the need for scheduling or attendance information.

Message: "I think we should proceed with the plan."
Category: IMPLICIT ACTION
Explanation: The message suggests proceeding with a plan, implying a recommended action for progressing a real estate transaction.

Message: "The budget details are attached."
Category: INFO SHARED
Explanation: The message provides information that budget details are attached, indicating transparency or sharing of information.

Explanation Examples:
Message: "When is the open house scheduled?"
Category: ASK
Explanation: Asks for the schedule of an open house event, common in the real estate market for showcasing properties to potential buyers.

Message: "Please prepare the contract for signing."
Category: ACTION REQUEST
Explanation: Instructs to prepare a contract for signing, indicating a step in finalizing a real estate deal between parties.
"""

# Initialize OpenAI API with your API key
openai.api_key = os.getenv('OPENAI_API_KEY')
client = OpenAI()

def classify_message_with_gpt4(message):
    # Clean and format the message
    cleaned_message = message.strip().lower()
    # Define the prompt with the user's message
    prompt = classification_prompt.format(message=cleaned_message)

    # Call OpenAI's model to classify the message
    response = client.chat.completions.create(
        model='gpt-4',
        messages=[
            {"role": "system", "content": classification_prompt},
            {"role": "user", "content": prompt}
        ],
        temperature=0,
    )

    # Extract the category and explanation from the model's response
    category_text = None
    explanation_text = None
    for message in response.choices[0].message.content.strip().split('\n'):
        if "Category:" in message:
            category_text = message.split(":")[-1].strip()
        elif "Explanation:" in message:
            explanation_text = message.split(":")[-1].strip()
    
    # If category is unrecognized, rerun the function
    if category_text not in [INFO_SHARED, ACTION_REQUEST, ASK, IMPLICIT_ACTION]:
        return classify_message_with_gpt4(message)
    
    return category_text, explanation_text
