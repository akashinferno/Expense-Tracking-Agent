# AI-Powered Google Sheets Expense Tracker

This project implements an AI-powered agent that automates expense tracking using natural language input. Users can type expenses in plain English, and the system automatically parses, categorizes, and logs them into Google Sheets.

## Features

- **Natural Language Processing**: Parse expenses like "lunch ₹200, cab ₹150, gave my friend 300"
- **AI-Powered Categorization**: Automatically categorizes expenses using LLM
- **Google Sheets Integration**: Direct logging to Google Sheets with real-time totals
- **Dynamic Calculations**: Running totals and summary calculations
- **Simple Terminal Interface**: Easy-to-use command-line interface

## Setup Instructions

### 1. Get Gemini API Key
1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Create a new API key
3. Add it to your `.env` file:
```
GEMINI_API_KEY=your_actual_api_key_here
```

### 2. Setup Google Sheets API
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select an existing one
3. Enable the Google Sheets API
4. Create credentials (OAuth 2.0 Client ID) for a desktop application
5. Download the credentials file and save it as `credentials.json` in this directory

### 3. Install Dependencies
```bash
pip install google-api-python-client google-auth google-generativeai python-dotenv google-auth-oauthlib google-auth-httplib2
```

### 4. Run the Application
```bash
python main.py
```

## Usage Examples

### Natural Language Input Examples:
- `lunch ₹200, coffee ₹50`
- `cab fare ₹150 today`
- `grocery shopping ₹800, medicines ₹300`
- `movie tickets ₹500, dinner ₹400 yesterday`


## Project Structure

```
expense-sheets-tracker/
├── main.py              # Main application
├── .env                 # Environment variables (API keys)
├── credentials.json     # Google API credentials (you need to add this)
├── token.pickle        # OAuth token (auto-generated)
└── README.md           # This file
```

## How It Works

1. **Input Processing**: User enters expense in natural language
2. **AI Parsing**: Gemini AI extracts structured data (item, amount, category, date)
3. **Sheet Integration**: Data is automatically added to Google Sheets
4. **Dynamic Calculations**: Running totals and summaries are updated automatically

## Categories

The system automatically categorizes expenses into:
- Food
- Transportation  
- Shopping
- Entertainment
- Health
- Bills
- Travel
- Other

## Security Notes

- Keep your API keys secure and never commit them to version control
- The `.env` file is ignored by git
- OAuth tokens are stored locally in `token.pickle`
