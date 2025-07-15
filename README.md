# Google Workspace Agent App

This Streamlit app lets you summarize Google Docs, Sheets, Slides, and PDF files from individual links or entire Google Drive folders (including subfolders). You can view summaries, and email the summary of a selected file or all files in a folder, directly from the app.

**Live App:** [https://app-workspace-agent-app.streamlit.app/](https://app-workspace-agent-app.streamlit.app/)

---

## Features
- Authenticate with Google Workspace (Drive, Docs, Sheets, Slides, Gmail)
- Summarize:
  - Individual Google Doc, Sheet, Drive, PDF, DOCX, XLSX, PPTX, or CSV files by link
  - All supported files in a Google Drive folder (recursively, including subfolders)
- Professional UI: two-column layout for Drive folders (file list on left, summary on right)
- Instantly view summaries for all files in a folder
- Email the summary of the selected file or all files in a folder to any recipient
- Supports custom SMTP credentials or uses Streamlit secrets

---

## Supported File Types
- Google Docs
- Google Sheets
- Google Slides
- Google Drive, 
- Google DOCX,
- Google XLSX,
- Google PPTX,
- Google CSV
- PDF files (text-based only; scanned/image PDFs are not supported for text extraction)

---

## Setup Instructions

### 1. Google Cloud Project & Service Account
- Go to the [Google Cloud Console](https://console.cloud.google.com/)
- Create a new project
- Enable the **Google Drive API**, **Gmail API**, **Google Sheets API**, **Google Docs API**, and **Google Slides API**
- Go to **APIs & Services > Credentials**
- Click **Create Credentials** > **Service account**
- Download the service account JSON and keep it safe
- Share any Google Docs/Sheets/Slides/PDFs or Drive folders you want to summarize with the service account email

### 2. Environment Variables / Secrets
- For local use: create a `.env` file or use `.streamlit/secrets.toml` with:
  - `GEMINI_API_KEY` (for Gemini summarization)
  - `GOOGLE_CREDENTIALS` (the service account JSON as a string)
  - `TARGET_EMAIL` (default recipient email)
  - SMTP credentials (optional, for custom email sending)
- For Streamlit Cloud: set these in the app's **Secrets** section

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the App Locally
```bash
streamlit run google_workspace_automation.py
```

---

## Usage
- Select the file type (Doc, Sheet, Slides, PDF, or Drive)
- Paste the shareable link (for Drive, use a folder link)
- For Drive folders, browse and select files in the left pane; summaries appear on the right
- Use the buttons to email the summary of the selected file or all files

---

## Emailing Summaries
- You can email the summary of the currently selected file
- Or email summaries of all files in a Drive folder (batch)
- Uses Gmail SMTP (default) or your custom SMTP credentials

---

## Deployment
- Deploy on [Streamlit Cloud](https://streamlit.io/cloud)
- Set all required secrets in the app's **Secrets** section
- App link: [https://app-workspace-agent-app.streamlit.app/](https://app-workspace-agent-app.streamlit.app/)

---

## Limitations
- PDF summarization works only for text-based PDFs (no OCR for scanned/image PDFs)
- Service account must have access to all files/folders you want to summarize
- Summaries are generated using Gemini API

---

## License
MIT 

---

### If you encounter any errors (e.g., missing packages, extraction issues), let me know and I’ll help you debug further!

**Try it out and let me know if you can now summarize all your files, including Office docs and slides!** 