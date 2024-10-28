import streamlit as st
import nltk
from main import get_response, html_comparison, load_html_file, save_html_file
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Ensure NLTK punkt resource is downloaded
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('all')

# Setup Google Sheets API client using credentials from secrets
def get_gspread_client():
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds_dict = {
        "type": st.secrets["type"],
        "project_id": st.secrets["project_id"],
        "private_key_id": st.secrets["private_key_id"],
        "private_key": st.secrets["private_key"],
        "client_email": st.secrets["client_email"],
        "client_id": st.secrets["client_id"],
        "auth_uri": st.secrets["auth_uri"],
        "token_uri": st.secrets["token_uri"],
        "auth_provider_x509_cert_url": st.secrets["auth_provider_x509_cert_url"],
        "client_x509_cert_url": st.secrets["client_x509_cert_url"]
    }
    creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
    client = gspread.authorize(creds)
    return client

# Access the Google Sheet
def get_google_sheet(client, spreadsheet_url):
    sheet = client.open_by_url(spreadsheet_url).sheet1  # Opens the first sheet
    return sheet

# Read the password from the first cell
def read_password_from_sheet(sheet):
    password = sheet.cell(1, 1).value  # Reads the first cell (A1)
    return password

# Update the password in the first cell
def update_password_in_sheet(sheet, new_password):
    sheet.update_cell(1, 1, new_password)  # Updates the first cell (A1) with the new password

# Initialize gspread client and access the sheet
client = get_gspread_client()
sheet = get_google_sheet(client, st.secrets["spreadsheet"])
PASSWORD = read_password_from_sheet(sheet)

# Initialize session state for authentication
if 'authenticated' not in st.session_state:
    st.session_state['authenticated'] = False
if 'password' not in st.session_state:
    st.session_state['password'] = PASSWORD
if 'reset_mode' not in st.session_state:
    st.session_state['reset_mode'] = False

# Function to check password
def check_password(password):
    return password == st.session_state['password']

# Password reset function
def reset_password(new_password, confirm_password):
    if new_password != confirm_password:
        st.error("Passwords do not match!")
    else:
        st.session_state['password'] = new_password
        update_password_in_sheet(sheet, new_password)
        st.session_state['reset_mode'] = False
        st.success("Password reset successfully!")

# Authentication block
if not st.session_state['authenticated']:
    st.title("Login to Proofreader")

    password_input = st.text_input("Enter Password", type="password")
    
    if st.button("Login"):
        if check_password(password_input):
            st.session_state['authenticated'] = True
            st.success("Login successful!")
        else:
            st.error("Incorrect password!")

    if st.button("Reset Password?"):
        st.session_state['reset_mode'] = True

# Reset password block
if st.session_state['reset_mode']:
    st.title("Reset Password")

    old_password = st.text_input("Enter Old Password", type="password")
    new_password = st.text_input("Enter New Password", type="password")
    confirm_password = st.text_input("Confirm New Password", type="password")
    
    if st.button("Reset Password"):
        if old_password == st.session_state['password']:
            reset_password(new_password, confirm_password)
        else:
            st.error("Incorrect old password!")
    
    if st.button("Back to Login"):
        st.session_state['reset_mode'] = False

if st.session_state['authenticated'] and not st.session_state['reset_mode']:
    # Streamlit UI for proofreading
    st.title("Proofreader")

    # Text area for chapter input
    chapter_text = st.text_area('Enter the text:')

    if st.button("Run Proofreading"):
        if chapter_text.strip():
            # Get response from proofreading API
            response = get_response(chapter_text)
            
            # Display the response (proofread text)
            st.markdown("### Proofread Text")
            st.text_area('Proofread Output:', response, height=300)

            # Generate HTML diff comparison
            html_pth = html_comparison(chapter_text, response)
            html_content = load_html_file(html_pth)

            # Add a download button for the HTML content
            st.download_button(
                label="Download Difference HTML",
                data=html_content,
                file_name="proofread_output.html",
                mime="text/html"
            )
        else:
            st.error("Please enter some text before running proofreading.")
