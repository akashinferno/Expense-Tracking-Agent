import json
import google.generativeai as genai
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import pickle
import os
from dotenv import load_dotenv

# Super simple expense tracker - beginner level!

# Load environment variables
load_dotenv()

# Get API key and Sheet ID from .env file
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
SHEET_ID = os.getenv('SHEET_ID')

def setup():
    # Setup Gemini
    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel("models/gemini-2.5-flash-lite")
    
    # Setup Google Sheets
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    
    if not creds or not creds.valid:
        flow = InstalledAppFlow.from_client_secrets_file(
            'credentials.json', 
            ['https://www.googleapis.com/auth/spreadsheets']
        )
        creds = flow.run_local_server(port=0)
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    
    service = build('sheets', 'v4', credentials=creds)
    return model, service

def parse_expense(model, text):
    # Ask AI to parse the expense
    prompt = f"""
    Parse: "{text}"
    Return only JSON: {{"items": [{{"item": "name", "amount": 100, "category": "Food"}}]}}
    Categories: Food, Transport, Shopping, Other
    """
    
    response = model.generate_content(prompt)
    json_text = response.text.strip()
    
    # Clean up response
    if '```json' in json_text:
        json_text = json_text.split('```json')[1].split('```')[0]
    if '```' in json_text:
        json_text = json_text.split('```')[1]
    
    return json.loads(json_text.strip())

def setup_sheet_headers(service):
    # Check if headers exist
    result = service.spreadsheets().values().get(
        spreadsheetId=SHEET_ID, 
        range='A1:F1'
    ).execute()
    
    if not result.get('values'):
        # Add headers and total cell
        headers = [
            ['Date', 'Item', 'Amount', 'Category', 'TOTAL:', '=SUM(C:C)']
        ]
        
        service.spreadsheets().values().update(
            spreadsheetId=SHEET_ID,
            range='A1:F1',
            valueInputOption='USER_ENTERED',
            body={'values': headers}
        ).execute()
        print("✅ Added headers with total formula")

def add_to_sheet(service, data):
    # Setup headers if they don't exist
    setup_sheet_headers(service)
    
    # Get next empty row
    result = service.spreadsheets().values().get(
        spreadsheetId=SHEET_ID, 
        range='A:A'
    ).execute()
    next_row = len(result.get('values', [])) + 1
    
    # Add each item (no running total column needed now)
    for item in data['items']:
        row = [[
            "Today",  # Date
            item['item'],  # Item name
            item['amount'],  # Amount
            item['category']  # Category
        ]]
        
        service.spreadsheets().values().update(
            spreadsheetId=SHEET_ID,
            range=f'A{next_row}:D{next_row}',
            valueInputOption='USER_ENTERED',
            body={'values': row}
        ).execute()
        
        print(f"Added: {item['item']} - ₹{item['amount']}")
        next_row += 1

def main():
    print("Simple Expense Tracker")
    print("----------------------")
    
    # Check if keys are set
    if not GEMINI_API_KEY:
        print("❌ Please set your GEMINI_API_KEY in the .env file!")
        return
    
    if not SHEET_ID or SHEET_ID == "your_sheet_id_here":
        print("❌ Please set your SHEET_ID in the .env file!")
        print("Create a Google Sheet and copy its ID from the URL")
        return
    
    model, service = setup()
    print("✅ Setup complete!")
    print("Type expenses like: lunch 200, cab 150")
    
    while True:
        expense = input("\nExpense (or 'quit'): ")
        
        if expense.lower() == 'quit':
            break
        
        try:
            parsed = parse_expense(model, expense)
            add_to_sheet(service, parsed)
            total = sum(item['amount'] for item in parsed['items'])
            print(f"Added total: ₹{total}")
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    main()