import streamlit as st
import nltk
from main import get_response, html_comparison, load_html_file, save_html_file

# Ensure NLTK punkt resource is downloaded
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('all')

# Streamlit UI
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
