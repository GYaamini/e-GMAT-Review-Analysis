import pandas as pd
import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()

# Data Preparation
def prepare_data():
    base_path = os.getcwd().split('backend')[0]
    file_path = os.path.join(base_path,"data_processing","e-GMAT_GMAT_Club_Reviews.csv")
    data = pd.read_csv(file_path)
    return data,base_path,file_path

# OpenRouter API Setup
OPENROUTER_API_KEY = os.getenv('API_KEY')
HEADERS = {
    "Authorization": f"Bearer {OPENROUTER_API_KEY}",
    "Content-Type": "application/json"
}

# LLM Function
def analyze_column(text, type):
    # model="anthropic/claude-3-sonnet"
    model="meta-llama/llama-3.3-8b-instruct:free"
    
    if type == 'Commended':
        prompt = f"""e-GMAT is a popular online platform for GMAT (Graduate Management Admission Test) preparation. 
        It's known for its personalized study plans, extensive video lessons, and AI-powered diagnostic tools, 
        making it a valuable resource for test takers seeking to improve their scores.
        Here is the strengths and praises in the review as content:
        Content:
        {text}
        
        Identify and give the following in short sentences or as bullet point:
        1. Top most mentioned strengths of the platform and features that are most appreciated by the users
        2. Top 2-3 courses which resulted in these commendable reviews. It is mentioned in the beginning of
            each review like-
            `Online Focused:
            content and question bank
            `
        3. Overall sentiment trend
        
        Instructions:
        1. Be precise and DO NOT omit the keywords
        2. Find them by how frequently or intensely they are mentioned and provide max 5-6 such strong 
            appreciation/praises given by users
        3. Arrange the points based on highest to lowest demand
        4. The available courses are Online 360, Online Focused, Mentorship, Online Intensive, and GMAT Live Prep.
        
        Analysis:
        """
    else:
        prompt = f"""e-GMAT is a popular online platform for GMAT (Graduate Management Admission Test) preparation. 
        It's known for its personalized study plans, extensive video lessons, and AI-powered diagnostic tools, 
        making it a valuable resource for test takers seeking to improve their scores.
        Here is the suggested improvements or recognized flaws in the user review as content:
        Content:
        {text}
        
        Identify and give the following in short sentences or as bullet point:
        1. Top most mentioned issues and flaws that should be addressed by the platform and Top features that are 
            bothering the users by blocking smooth learning experience
        2. Top 2-3 courses which resulted in these shortcomings. It is mentioned in the beginning of
            each review like-
            `Online 360:
            i feel the quant section needs to be re-evaluated.
            the estimated course durations are not accurate.
            the study plan set for me was far from realistic.
            `
        3. Overall sentiment trend
        
        Instructions:
        1. Be precise and DO NOT omit the keywords.
        2. Find them by how frequently or intensely they are mentioned and provide max 5 such strong 
            suggestions/improvements demanded by users
        3. Arrange the points based on highest to lowest demand
        4. the available courses are Online 360, Online Focused, Mentorship, Online Intensive, and GMAT Live Prep.  
        
        Analysis:
        """
    
    payload = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.1  # More deterministic for analysis
    }
    
    response = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers=HEADERS,
        data=json.dumps(payload)
    )
    print("open router response done")
    return response.json()['choices'][0]['message']['content']

# Workflow
def get_timestamp(file_path):
    try:
        with open(file_path, 'r') as file:
            first_line = file.readline().strip()
            return float(first_line)
    except Exception as e:
        print(f"Error reading cached timestamp: {e}")
        return None
    
def process_reviews(type):
    df,base_path,csv_path = prepare_data()
    file_path_SA = os.path.join(base_path,"data_processing","strengths_analysis.txt")
    file_path_FR = os.path.join(base_path,"data_processing","feature_recommendations.txt")
    file_path = file_path_SA if type == 'Commended' else file_path_FR
    
    csv_timestamp = os.path.getmtime(csv_path)
    
    timestamp = get_timestamp(file_path)
    
    if timestamp is None or csv_timestamp > timestamp:
        print("CSV file has changed. Regenerating analysis...")
        
        combined_text = "\n\n".join(df[type].tolist())
        analysis = analyze_column(combined_text[:15000], type)  # Truncate to avoid token limits
        
        try:
            with open(file_path, 'w') as file:
                # timestamp as the first line
                file.write(f"{csv_timestamp}\n")  
                file.write(analysis)
        except Exception as e:
            print(f"Error writing analysis with timestamp: {e}")

        print("Processing reviews done (llm extraction)")

    else:
        print("CSV file has not changed. Loading stored analysis...")
        
        with open(file_path, 'r') as file:
            # Skip the timestamp get the rest of the content
            analysis = file.read().strip().split('\n', 1)[1]
        
        print("Processing reviews done (stored extraction)")
    return analysis

def process_gathering(type):
    df = prepare_data()
    combined_text = "\n\n".join(df[type].tolist())[:15000] # Truncate to avoid token limits

    return combined_text
