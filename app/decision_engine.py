import requests
from config import DECISION_ENGINE_URL

def submit_to_decision_engine(application_data):
    # Process application data and calculate preAssessment value
    pre_assessment = calculate_pre_assessment(application_data['balance_sheet'])
    
    # Prepare data for submission to decision engine
    decision_data = {
        "business_details": application_data['business_details'],
        "preAssessment": pre_assessment
    }
    
    # Submit data to decision engine
    response = requests.post(DECISION_ENGINE_URL, json=decision_data)
    return response.json()

def calculate_pre_assessment(balance_sheet_data):
    last_12_months_data = balance_sheet_data[-12:]  # Select the last 12 months of data

    total_profit = sum(entry['profitOrLoss'] for entry in last_12_months_data)
    average_assets = sum(entry['assetsValue'] for entry in last_12_months_data) / 12

    if total_profit > 0:
        pre_assessment = "60"
    elif average_assets > loan_amount:  # Assuming you have access to the loan amount
        pre_assessment = "100"
    else:
        pre_assessment = "20"

    return pre_assessment

