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
  
  # Set up Gemini API
    
  # genai.configure(api_key='AIzaSyB4wOYqbnQ0UynxmCWua17tlY78j9sx7IU')
  
  # # Set up Gemini model and prompt
  # model = genai.GenerativeModel('gemini-1.5-flash')
  api_key =  st.secrets["Openai_api"]
  client = OpenAI(
        # This is the default and can be omitted
        api_key = api_key
    )
  
  # Set up OpenAI model and prompt
  model="gpt-4o-mini-2024-07-18"
  prompt_1 = """ I have a manuscript that needs thorough editing. Please perform the following tasks on the text provided:

1) Copy-Editing and Line Editing:

- Correct all spelling, grammatical, and capitalization errors. Use British English spellings unless otherwise specified.
Example: Use "analyse" not "analyze"; "organisation" not "organization."
- Fix repetitive word usage and improve word choices while preserving the original meaning.
Example: Replace "comprise of" with "comprise."
- Ensure proper arrangement of adjectives: opinion > size > age > shape > color > origin > material > purpose.
Example: "A beautiful large antique wooden dining table."

2)Punctuation:

- Use Oxford commas in lists.
Example: "I bought apples, oranges, and bananas."
- Apply em dashes (—) for emphasis or parenthetical clauses.
Example: "She had one goal—to succeed."
- Use en dashes (–) for number ranges or reciprocal relationships.
Example: "1914–18 war" or "Mumbai–Pune highway."
- Write ellipses as three dots separated by spaces: . . .
Example: "I was thinking . . . but stopped."
- Use single quotes (‘ ’) for direct speech and double quotes (“ ”) for quotes within quotes.
Example: ‘He said, “This is important.”’
- Place punctuation correctly inside or outside quotation marks:
Example (full sentence): ‘She said, “This is perfect.”’
Example (partial): She described it as ‘perfect’.

3) Consistency in Style:

Follow these capitalization rules:
- Titles: "President of the United States" but "the president of a company."
Geographical regions: "North-eastern states" but "north-east direction."
- Italicize:
Non-OED vernacular/local words (on first use only): dal, naan.
Titles of books, films, and newspapers: Pride and Prejudice, the Times of India.
- Maintain correct hyphenation:
Example: "north-east" but "North-eastern states."
- Write dates in the format "dd month yyyy." Use no apostrophe for decades like '1990s'. For abbreviated decades, use a single close quote as in '90s'.
Example: "15 August 1947."
- Spell out numbers from zero to ninety-nine, and use numerals for numbers above 100.
Example: "Seventy-five" but "125."

4) Proofreading:

- Eliminate non-sequiturs:
Example: Incorrect: "He lived in Delhi, was tall, and drove a car." Correct: "He was tall, lived in Delhi, and drove a car."
- Avoid dangling modifiers:
Example: Incorrect: "Handing me the book, his smile widened." Correct: "As he handed me the book, his smile widened."
- Remove stylistic issues or mixed metaphors:
Example: Incorrect: "Virgin territory pregnant with possibilities." Correct: "Unexplored territory full of potential."
- Fix any inconsistencies in tenses of the words used and dont make any unnecessary changes in the phrases used by the author.

5) Apply these rules to the text and provide the corrected version without additional comments or suggestions. 
6) Make sure you make minimal changes to the text and dont change the authors writing style. Ensure the length of the text remains the same.
Here is the Chapter text: <<ChapterText>>
"""
  prompt1 = prompt_1.replace('<<ChapterText>>', chapter)
  # response = model.generate_content(prompt)

  # return response.text
  chat_completion1 = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": prompt1,
            }
        ],
        model=model,
	temperature = 0
    )

  response1 = chat_completion1.choices[0].message.content

  prompt_2 = """ I have a manuscript that needs thorough editing. Please perform the following tasks on the text provided:

1) Dialogue and Quotation:

- Use proper dialogue formatting:
Example: ‘He said, “I will join you tomorrow.”’
- Format trailing speech with ellipses:
Example: "I’m not sure . . ."
- Place punctuation correctly within or outside quotes:
Example (full sentence): ‘She said, “This is wonderful.”’
Example (phrase): He referred to it as ‘amazing’.

2) Acronyms and Abbreviations:

- Spell out acronyms upon first use:
Example: "National Aeronautics and Space Administration (NASA)" initially, then "NASA."
- Use stops for abbreviated names but not acronyms:
Example: "A.P.J. Abdul Kalam" but "NASA."
- Use stops for "e.g.", "i.e.", but not for measurements like "7 cm."

3) Bias and Legal Compliance:

- Remove gender or regional bias. Use neutral language:
Example: Replace "chairman" with "chairperson."
- Flag potentially libelous statements or those with harmful stereotypes.

4) Apply Advanced Style Guide Rules:

- Correct commonly misused words:
Example: Use "affect" (verb) for "influence" and "effect" (noun) for "result."
Use "stationery" (writing materials) instead of "stationary" (not moving).
- Maintain British spelling conventions:
Example: "Programme" not "program" (except "computer program").
- Use correct forms of commonly confused terms:
Example: "Licence" (noun) vs. "license" (verb).

5) Place Names and Standardization:

- Use updated place names unless in historical context:
Example: "Mumbai" not "Bombay"; "Kolkata" not "Calcutta."
- Ensure proper capitalization for regions and entities:
Example: "South Asia" but "southward direction."

6) Headlines and Titles:

- Follow these capitalization rules:
Capitalize nouns, verbs, and pronouns.
- Lowercase prepositions, conjunctions, and articles unless the first word.
Example: "The Rise and Fall of Empires."

7) Apply these rules to the text and provide the corrected version without additional comments or suggestions. 
8) Make sure you make minimal changes to the text and dont change the authors writing style. Ensure the length of the text remains the same.
Here is the Chapter text: <<ChapterText>>
"""
  prompt2 = prompt_2.replace('<<ChapterText>>', response1)
  # response = model.generate_content(prompt)

  # return response.text
  chat_completion2 = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": prompt2,
            }
        ],
        model=model,
	temperature = 0
    )

  response = chat_completion2.choices[0].message.content
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



