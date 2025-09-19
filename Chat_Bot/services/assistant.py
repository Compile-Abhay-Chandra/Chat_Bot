import webbrowser
from . import musicLibrary
from .news_api import fetch_random_news as news
from .llama_test import query_model as response
# import google.generativeai as genai

# Configure Gemini AI
# genai.configure(api_key="AIzaSyAotC4M-yePA_K2mHbNr_1pe3Y-M8pNmSE")
# model = genai.GenerativeModel("gemini-1.5-flash")

# def AI(query: str) -> str:
#     """Send query to Gemini AI and return response."""
#     response = model.generate_content(query + "\nPlease provide a short reply.")
#     return response.text

def process_command(command: str, pdf_text: str = None) -> str:
    """Process user command and return response text. If pdf_text is provided, use it for context."""
    try:
        c = command.lower()

        if "open google" in c:
            webbrowser.open("https://google.com")
            return "Opening Google..."
        elif "open youtube" in c:
            webbrowser.open("https://youtube.com")
            return "Opening YouTube..."
        elif "news" in c:
            return news("f5e28cedb4f54e23a37e762df0e86b92", country="us")
        elif c.startswith("play"):
            song = c.split(" ")[1]
            link = musicLibrary.music.get(song)
            if link:
                webbrowser.open(link)
                return f"Playing {song}..."
            else:
                return "Song not found."
        else:
            if pdf_text:
                # Pass the PDF text as context to the model
                prompt = f"Based on the following PDF content, answer the user's question.\nPDF Content:\n{pdf_text}\n\nUser Question: {command}"
                return response(prompt)
            else:
                return response(command)

    except Exception as e:
        return f"Error: {e}"
