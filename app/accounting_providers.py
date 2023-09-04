import requests
from config import XERO_API_KEY, MYOB_API_KEY

def fetch_balance_sheet(application_id, provider):
    if provider == 'xero':
        api_key = XERO_API_KEY
        headers = {'Authorization': f'Bearer {api_key}'}
        params = {'application_id': application_id}
        response = requests.get('https://xero-api.com/balance-sheet', headers=headers, params=params)
        balance_sheet_data = response.json()
        return balance_sheet_data
    elif provider == 'myob':
        api_key = MYOB_API_KEY
        headers = {'Authorization': f'Bearer {api_key}'}
        params = {'application_id': application_id}
        response = requests.get('https://myob-api.com/balance-sheet', headers=headers, params=params)
        balance_sheet_data = response.json()
        return balance_sheet_data
    else:
        return None

