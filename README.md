# BlaBla Fish Readme

This code is a Streamlit application that allows users to upload a PDF file, extract text from the PDF, translate the text into French while preserving the original formatting, and save the translated text to a text file.

## Requirements
- Python 3.x
- `streamlit` 
- `dotenv` 
- `re` 
- `PyPDF2` 
- `openai (0.28)` 

## Instructions
1. Install the required libraries using `pip`:
    ```
    pip install streamlit python-dotenv PyPDF2 openai
    ```
2. Obtain an OpenAI API key and store it in a `.env` file in the same directory as the script:
    ```
    OPENAI_API_KEY=your_api_key_here
    ```
3. Run the Streamlit application using the following command:
    ```
    streamlit app.py
    ```
4. Upload a PDF file using the provided file uploader.
5. The app will extract text from the PDF, translate the text into French using GPT-3, and save the translated text to a text file.

## Functionality
- The code uses GPT-3 Chat Completion to translate text into French.
- It handles API errors, specifically retries on a 502 Bad Gateway error.
- Progress bars are displayed for text extraction and translation progress.
- Translation is done preserving the original formatting of the text.