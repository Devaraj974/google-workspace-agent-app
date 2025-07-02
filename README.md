# Google Workspace Automation with CrewAI

This project automates the process of reading your latest Google Doc and Sheet, summarizing their content, and sending the summary via Gmail using CrewAI and OpenAI's GPT-4o.

## Features
- Authenticates with Google Workspace (Drive, Sheets, Gmail)
- Finds the most recent Google Doc and Google Sheet
- Reads and summarizes their content using GPT-4o
- Sends the summary to a target email via Gmail

## Setup Instructions

### 1. Google Cloud Project & OAuth Credentials
- Go to the [Google Cloud Console](https://console.cloud.google.com/)
- Create a new project
- Enable the **Google Drive API**, **Gmail API**, and **Google Sheets API**
- Go to **APIs & Services > Credentials**
- Click **Create Credentials** > **OAuth client ID**
- Choose **Desktop app**
- Download the credentials JSON and rename it to `credentials.json`
- Place `credentials.json` in the project directory

### 2. Environment Variables
- Copy `.env.example` to `.env`
- Fill in your OpenAI API key and the target email address

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the Script
```bash
python google_workspace_automation.py
```
- On first run, a browser window will open for Google authentication.
- Grant access to the requested scopes.
- A `token.pickle` file will be created for future runs.

## Notes
- The script uses CrewAI agents for modular, explainable automation.
- You need access to the Google account with the Docs/Sheets you want to process.
- The summary is sent to the email specified in your `.env` file.

## Troubleshooting
- Ensure `credentials.json` is present in the project directory.
- If you change Google account or permissions, delete `token.pickle` and re-run the script.

## License
MIT 