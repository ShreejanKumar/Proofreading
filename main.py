import pathlib
import textwrap
import google.generativeai as genai
from IPython.display import display
from IPython.display import Markdown
import difflib
import nltk
import streamlit as st


# Ensure NLTK downloads 'punkt' properly
nltk.download('punkt')

def get_response(chapter):
  
  # Set up Gemini API
    
  genai.configure(api_key=st.secrets["Gemini_api"])
  
  # Set up Gemini model and prompt
  model = genai.GenerativeModel('gemini-1.5-flash')
  prompt_template = """ I have a manuscript that needs thorough editing. Please perform the following tasks on the text provided:

1) Copy-Editing and Line Editing: Correct any spelling, grammatical, and capitalization errors. Fix repetitive word usage and correct any inappropriate word choices. Fix punctuation errors, ensuring correct use of commas, semicolons, and other punctuation marks. Verify factual information and correct as necessary.
2) Proofreading: Ensure the text is free from stylistic issues that might affect readability. Maintain consistent layout, typography, and spacing. Correct any errors in captioning and ensure the correct use of bold and italics.
3) Final Checks and Coordination: Apply consistent orthography and capitalization rules. Ensure correct dialogue formatting, including proper use of quotation marks and ellipses for trailing speech. Provide the edited text directly without any additional comments or suggestions.
4) Make as little changes as you can. It is important to preserve the writing style of the author.
5) Keep the length of the text same as original. No need to summarize or shorten it.
6) Write years and dates as numerals in 'dd month yyyy' format. Use no apostrophe for decades like '1990s'. For abbreviated decades, use a single close quote as in '90s'.

Here is the Chapter text: <<ChapterText>>
"""
  prompt = prompt_template.replace('<<ChapterText>>', chapter)
  response = model.generate_content(prompt)

  return response.text

def split_into_sentences(text):
    nltk.download('punkt')
    return nltk.tokenize.sent_tokenize(text)

def side_by_side_diff(string1, string2):
    # Split the input strings into sentences
    sentences1 = split_into_sentences(string1)
    sentences2 = split_into_sentences(string2)
    nltk.download('punkt')
    # Create an HtmlDiff object
    diff = difflib.HtmlDiff()

    # Use make_file to generate a side-by-side HTML comparison
    html_diff = diff.make_file(sentences1, sentences2, context=True, numlines=2)
    return html_diff

def html_comparison(chapter, response):
    # Download the tokenizer
    nltk.download('punkt')
    html_output = side_by_side_diff(chapter, response)
    html_pth = 'diff_output.html'
    with open(html_pth, 'w') as file:
        file.write(html_output)
    return html_pth


def load_html_file(file_path):
    """Load the content of the HTML file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    except UnicodeDecodeError:
        # Try reading with a different encoding if utf-8 fails
        with open(file_path, 'r', encoding='windows-1252') as file:
            return file.read()
    except FileNotFoundError:
        st.error(f"The file {file_path} does not exist.")
        return ""

def save_html_file(file_path, content):
    """Save the content to the HTML file."""
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(content)









