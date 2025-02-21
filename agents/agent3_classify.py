# agents/agent3_classify.py
"""
Agent 3: Accident Classifier with Reasoning using o3-mini

This agent receives the improved text from Agent 2 and uses the o3-mini model to analyze the text,
explain its reasoning step by step, and determine the most likely accident cause along with a confidence score.

Process:
1. The improved text is sent to the OpenAI Chat API using the o3-mini model (e.g., "o3-mini-2025-01-31")
   to generate a semantic analysis.
2. The model explains its reasoning step by step based on the following list of candidate causes:
   - Driver distraction
   - Speeding
   - Driving under the influence of alcohol or drugs
   - Disregard for traffic rules
   - Fatigue and drowsiness
   - Lack of vehicle maintenance
   - Adverse weather conditions
   - Inadequate infrastructure
   - Aggressive behavior
   - Lack of experience
   - Inadequate use of safety equipment
   - Animals on the road
   - Visibility issues
   - Disregard for right of way
   - Improper lane usage
   - Lack of attention to pedestrians and cyclists
   - Driver health issues
   - Pedestrian inattention
   - Others
3. The model returns a chain-of-thought explanation, the selected cause, and a confidence score between 0 and 1.
"""

import openai
from config import OPENAI_API_KEY

openai.api_key = OPENAI_API_KEY

def agent3_classify(text: str) -> dict:
    # Candidate causes list
    causes = [
        "Driver distraction",
        "Speeding",
        "Driving under the influence of alcohol or drugs",
        "Disregard for traffic rules",
        "Fatigue and drowsiness",
        "Lack of vehicle maintenance",
        "Adverse weather conditions",
        "Inadequate infrastructure",
        "Aggressive behavior",
        "Lack of experience",
        "Inadequate use of safety equipment",
        "Animals on the road",
        "Visibility issues",
        "Disregard for right of way",
        "Improper lane usage",
        "Lack of attention to pedestrians and cyclists",
        "Driver health issues",
        "Pedestrian inattention",
        "Others"
    ]
    
    system_message = (
        "You are a data science assistant specialized in analyzing road accident descriptions. "
        "Your task is to determine the most likely accident cause from the following list: " +
        ", ".join(causes) +
        ". Please explain your reasoning step by step and then provide the selected cause and a confidence score between 0 and 1."
    )
    
    user_message = (
        f"Accident Description: {text}\n\n"
        "Provide your step-by-step reasoning, the selected cause, and the confidence score in the following format:\n"
        "Step-by-step reasoning: ...\n"
        "Selected Cause: ...\n"
        "Score: ..."
    )
    
    messages = [
        {"role": "system", "content": system_message},
        {"role": "user", "content": user_message}
    ]
    
    response = openai.ChatCompletion.create(
        model="gpt-4o",  
        messages=messages,
        temperature=0.3,
        max_tokens=300
    )
    
    result = response["choices"][0]["message"]["content"]
    
    # Return the complete explanation (chain-of-thought, selected cause, and score)
    return {"explanation": result}
