import streamlit as st
from dotenv import load_dotenv
import re
from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter
import openai
import os
import time

def chatbotGPT3_with_retry(conversation, model="gpt-3.5-turbo-0125", temperature=0, max_tokens=4000):
    MAX_RETRIES = 3
    DELAY_SECONDS = 600
    retries = 0
    while retries < MAX_RETRIES:
        try:
            response = openai.ChatCompletion.create(model=model, messages=conversation, temperature=temperature, max_tokens=max_tokens)
            text = response['choices'][0]['message']['content']
            return text, response['usage']['total_tokens']
        except openai.error.APIError as e:
            if e.status_code == 502:  # Bad Gateway
                retries += 1
                time.sleep(DELAY_SECONDS * retries)
            else:
                raise  # Re-raise the error if it's not a 502 error or retry limit exceeded
    raise Exception("Maximum retry limit exceeded")

# def ensure_userprofile_exists(filepath):
#     # Check if the file exists
#     if not os.path.exists(filepath):
#         # Create the directory if it doesn't exist
#         os.makedirs(os.path.dirname(filepath), exist_ok=True)
#         # Create the file since it doesn't exist
#         with open(filepath, 'w', encoding='utf-8') as f:
#             # You can initialize the file with default content if necessary
#             f.write('')  # Write an empty string or initial content


load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")


# uploading
pdf = st.file_uploader("upload here", type="pdf")

# Check if it has stuff in it and extract it
if pdf is not None:
    # Get the file name, replace non-alphanumeric characters with underscores
    file_name = re.sub(r'\W+', '_', pdf.name)
    # Remove the .pdf extension, if present
    file_name = re.sub(r'\.pdf$', '', file_name, flags=re.IGNORECASE)
    translate_name = f'{file_name}.txt'

    pdf_Reader = PdfReader(pdf)
    text = ""
    total_pages = len(pdf_Reader.pages)  # Get total number of pages
    progress_bar_text_extraction = st.progress(0)  # Create a progress bar for text extraction
    progress_bar_text_extraction.text("Text Extraction Progress")  # Label the progress bar

    # loop through pages
    for i, page in enumerate(pdf_Reader.pages, start=1):
        # concatenate is a funny word
        text += page.extract_text()
        # Update progress
        progress_bar_text_extraction.progress(i / total_pages)

    # split into chunks 
    text_splitter = CharacterTextSplitter(
        separator="\n",
        chunk_size=2000,
        chunk_overlap=0,
        length_function=len
    )

    # create a thing to hold the chunks in an array
    chunks = text_splitter.split_text(text)

    processed_chunks = set()  # Set to keep track of processed chunks
    progress_bar_translations = st.progress(0)  # Progress bar for translations
    progress_bar_translations.text("Translation Progress")  # Label the progress bar

    for i, chunk in enumerate(chunks, start=1):
        # Check if the chunk has already been processed
        if chunk not in processed_chunks:
            # Translate the chunk to French
            translate_prompt = [{'role': 'system', 'content': "Translate given text into French while preserving the original formatting as closely as possible."}, {'role': 'user', 'content': chunk}]
            translated_chunk, tokens_risk = chatbotGPT3_with_retry(translate_prompt)

            # Append translated chunk to the file
            with open(translate_name, "a", encoding="utf-8") as file:
                file.write(translated_chunk)

            # Add the chunk to the set of processed chunks
            processed_chunks.add(chunk)
        
        # Update translation progress
        progress_bar_translations.progress(i / len(chunks))
