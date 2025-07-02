import os
import pickle
import base64
from email.mime.text import MIMEText
import streamlit as st
from dotenv import load_dotenv  # Optional, but not used for secrets now
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
import google.generativeai as genai
from langgraph.graph import StateGraph, END
from typing import TypedDict

# --- Streamlit Page Config ---
st.set_page_config(page_title="Google Workspace Agent App", page_icon="🤖")
st.title("Google Workspace Agent App")
st.markdown("""
Summarize a Google Doc, Sheet, or Slides and email the summary using an agent-based workflow!\
**Your data is processed securely.**
""")

st.info("""
**Instructions:**
1. Select the Google file type (Doc, Sheet, or Slides).
2. Paste the shareable link (ensure the file is accessible to the app's Google account).
3. Click 'Summarize and Email (Agent)'.
""")

# --- Load secrets from Streamlit secrets ---
GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]
TARGET_EMAIL = st.secrets["TARGET_EMAIL"]
GOOGLE_CREDENTIALS = st.secrets["GOOGLE_CREDENTIALS"]  # Should be the JSON string

SCOPES = [
    'https://www.googleapis.com/auth/drive.readonly',
    'https://www.googleapis.com/auth/gmail.send',
    'https://www.googleapis.com/auth/spreadsheets.readonly',
    'https://www.googleapis.com/auth/presentations.readonly',
    'https://www.googleapis.com/auth/documents.readonly'
]

# --- Write Google credentials to file at runtime ---
CREDENTIALS_PATH = "credentials.json"
with open(CREDENTIALS_PATH, "w") as f:
    f.write(GOOGLE_CREDENTIALS)

# --- Google Auth ---
def get_credentials():
    creds = None
    token_path = "token.pickle"
    if os.path.exists(token_path):
        with open(token_path, 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_PATH, SCOPES)
            creds = flow.run_local_server(port=0)
        with open(token_path, 'wb') as token:
            pickle.dump(creds, token)
    return creds

# --- Extraction Functions ---
def extract_doc_text(docs_service, doc_id):
    try:
        doc = docs_service.documents().get(documentId=doc_id).execute()
        text = []
        for element in doc.get('body', {}).get('content', []):
            if 'paragraph' in element:
                for p_elem in element['paragraph'].get('elements', []):
                    if 'textRun' in p_elem:
                        text.append(p_elem['textRun'].get('content', ''))
        return ''.join(text)
    except Exception as e:
        return f"Error reading Google Doc: {e}"

def extract_sheet_text(sheets_service, sheet_id):
    try:
        result = sheets_service.spreadsheets().values().get(
            spreadsheetId=sheet_id, range='A1:Z1000').execute()
        values = result.get('values', [])
        sheet_data = ""
        if values:
            for row in values:
                sheet_data += "\t".join([str(cell) for cell in row]) + "\n"
        return sheet_data
    except Exception as e:
        return f"Error reading Google Sheet: {e}"

def extract_presentation_text(slides_service, presentation_id):
    try:
        presentation = slides_service.presentations().get(presentationId=presentation_id).execute()
        slides = presentation.get('slides', [])
        text_content = []
        for i, slide in enumerate(slides):
            elements = slide.get('pageElements', [])
            for element in elements:
                shape = element.get('shape')
                if shape:
                    text_elements = shape.get('text', {}).get('textElements', [])
                    for te in text_elements:
                        if 'textRun' in te:
                            text_content.append(te['textRun'].get('content', ''))
        return '\n'.join(text_content)
    except Exception as e:
        return f"Error reading Google Slides: {e}"

# --- LangGraph State Schema ---
class AgentState(TypedDict):
    file_type: str
    file_id: str
    extracted_text: str
    summary: str
    email_status: str

# --- LangGraph Nodes ---
def fetch_content_node(state: AgentState):
    creds = get_credentials()
    file_type = state['file_type']
    file_id = state['file_id']
    text = ""
    if file_type == "Doc":
        docs_service = build('docs', 'v1', credentials=creds)
        text = extract_doc_text(docs_service, file_id)
    elif file_type == "Sheet":
        sheets_service = build('sheets', 'v4', credentials=creds)
        text = extract_sheet_text(sheets_service, file_id)
    elif file_type == "Slides":
        slides_service = build('slides', 'v1', credentials=creds)
        text = extract_presentation_text(slides_service, file_id)
    state['extracted_text'] = text
    return state

def summarize_node(state: AgentState):
    genai.configure(api_key=GEMINI_API_KEY)
    text = state.get('extracted_text', '')
    file_type = state.get('file_type', '')
    prompt = f"Summarize the following Google {file_type} content:\n\n{text}\n\nSummary:"
    try:
        model = genai.GenerativeModel('models/gemini-1.5-pro-latest')
        response = model.generate_content(prompt)
        summary = response.text
    except Exception as e:
        summary = f"Error generating summary: {e}"
    state['summary'] = summary
    return state

def email_node(state: AgentState):
    summary = state.get('summary', '')
    creds = get_credentials()
    gmail_service = build('gmail', 'v1', credentials=creds)
    try:
        message = MIMEText(summary)
        message['to'] = TARGET_EMAIL
        message['from'] = 'me'
        message['subject'] = 'Automated Google Workspace Summary'
        raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
        body = {'raw': raw_message}
        gmail_service.users().messages().send(userId='me', body=body).execute()
        state['email_status'] = "Gmail email sent successfully!"
    except Exception as e:
        state['email_status'] = f"Error sending Gmail: {e}"
    return state

# --- Streamlit UI ---
file_type = st.selectbox("Select the file type to summarize:", ["Doc", "Sheet", "Slides"])
link = st.text_input(f"Paste the Google {file_type} link here:")

# Helper to extract ID from link
def extract_id_from_link(link):
    try:
        parts = link.split("/d/")
        if len(parts) > 1:
            return parts[1].split("/")[0]
        else:
            return ""
    except Exception:
        return ""

if st.button("Summarize and Email (Agent)"):
    if not link:
        st.error("Please paste a valid Google link.")
    else:
        file_id = extract_id_from_link(link)
        if not file_id:
            st.error("Could not extract file ID from the link. Please check the link format.")
        else:
            # --- LangGraph Agent Workflow ---
            graph = StateGraph(AgentState)
            graph.add_node('fetch', fetch_content_node)
            graph.add_node('summarize', summarize_node)
            graph.add_node('email', email_node)
            graph.add_edge('fetch', 'summarize')
            graph.add_edge('summarize', 'email')
            graph.add_edge('email', END)
            graph.set_entry_point('fetch')
            app = graph.compile()
            st.info("Running agent workflow...")
            result = app.invoke({
                "file_type": file_type,
                "file_id": file_id,
                "extracted_text": "",
                "summary": "",
                "email_status": ""
            })
            st.subheader("Summary:")
            st.write(result.get('summary', ''))
            if "successfully" in result.get('email_status', '').lower():
                st.success(result.get('email_status', ''))
            else:
                st.error(result.get('email_status', '')) 