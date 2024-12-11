import pathlib
import textwrap
import google.generativeai as genai
from IPython.display import display
from IPython.display import Markdown
import difflib
import nltk
import streamlit as st
from difflib import SequenceMatcher
from openai import OpenAI


# Ensure NLTK downloads 'punkt' properly
nltk.download('punkt')

def get_response(chapter):
  
  # # Set up Gemini model and prompt
  # model = genai.GenerativeModel('gemini-1.5-flash')
  api_key =  st.secrets["Openai_api"]
  client = OpenAI(
        # This is the default and can be omitted
        api_key = api_key
    )
  
  # Set up OpenAI model and prompt
  model="gpt-4o-mini-2024-07-18"
  prompt_template = """ I have a manuscript that needs thorough editing. Please perform the following tasks on the text provided:

1) Copy-Editing and Line Editing: Correct any spelling, grammatical, and capitalization errors. Fix repetitive word usage and correct any inappropriate word choices.
2) Fix all punctuation errors, ensuring correct use of commas, semicolons, colons, periods, quotation marks, and other punctuation marks.
3) Fix any inconsistencies in tenses of the words used and dont make any unnecessary changes in the phrases used by the author.
4) Proofreading: Ensure the text is free from stylistic issues. Maintain consistent layout, typography, and spacing. Correct any errors in captioning and ensure the correct use of bold and italics.
5) Final Checks and Coordination: Apply consistent orthography and capitalization rules. Ensure correct dialogue formatting, including proper use of quotation marks and ellipses for trailing speech. Provide the edited text directly without any additional comments or suggestions.
6) Make as little changes as you can. It is important to preserve the writing style of the author.
7) Keep the length of the text same as original. No need to summarize or shorten it.
8) Write years and dates as numerals in 'dd month yyyy' format. Use no apostrophe for decades like '1990s'. For abbreviated decades, use a single close quote as in '90s'.
9) Insert em dashes where appropriate, in place of commas, colons, or parentheses. They can be used to emphasize or draw attention to material, or to set off additional information. Eg: “Of course you have a point,” Mabel murmured. “That is—I suppose it is concerning.” Here it represents hesitation.
10) Preserve correctly hyphenated words (e.g., "south-east Asia") and avoid unnecessary changes to hyphenation. Do not alter hyphenated terms that are correctly used.
Here is the Chapter text: <<ChapterText>>
"""
  prompt = prompt_template.replace('<<ChapterText>>', chapter)
  # response = model.generate_content(prompt)

  # return response.text
  chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        model=model,
	temperature = 0
    )

  response = chat_completion.choices[0].message.content
  return response

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


def similarity_ratio(original, edited):
    return SequenceMatcher(None, original, edited).ratio()



