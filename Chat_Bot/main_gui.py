import tkinter as tk
import speech_recognition as sr
import threading
import google.generativeai as genai
import webbrowser
import pyttsx3
import musicLibrary
from news_api import fetch_random_news as news
from gtts import gTTS
import pygame
import os
from tkinter import PhotoImage                        # new line
# from PIL import Image, ImageTk

# Create the main window
root = tk.Tk()
root.title("A.I Assistant")

# Set the size of the window
root.state('zoomed')

# Set the background color of the window
root.configure(bg='#a0928f')

recognizer = sr.Recognizer()
engine = pyttsx3.init()






# Create an event to control stopping

stop_event = threading.Event()


def replace_last_line(new_text, color=None, size=15):
    # Replace the last line in the output box with new text.
    label_output.config(state=tk.NORMAL)
    try:
        # Delete the last line (e.g., "Listening...")
        label_output.delete("end-2l", "end-1l")
    except tk.TclError:
        pass  # Ignore if no text to delete

    # Add the new text
    label_output.insert(tk.END, new_text + "\n")
    if color:
        label_output.tag_configure(color, foreground=color, font=("Helvetica", size))
        label_output.tag_add(color, "end-2l", "end-1l")

    label_output.see("end")  # Ensure the new text is visible
    label_output.config(state=tk.DISABLED)


def speech_to_text():
    global is_listening
    try:
        with sr.Microphone() as source:
            # Insert the "Listening..." message
            temp_tag = "listening_tag"
            update_output("Listening...", align="right", color="green", size=20, temp_tag=temp_tag)
            
            # Use the microphone stream directly for control
            while not stop_event.is_set():  # Check if the stop_event is triggered
                try:
                    audio = recognizer.listen(source, timeout=1, phrase_time_limit=5)
                    word = recognizer.recognize_google(audio)
                    
                    # Check if the recognized word is "activate"
                    if word.lower() == "stop":
                        on_off_button_toggle()

                    # Replace "Listening..." text with recognized text
                    replace_last_line(word, color="blue", size=20)
                    recognized_text.set(word)  # Store recognized text
                    processCommand(word)  # Process the command
                    break  # Exit the loop after successful recognition
                    

                except sr.WaitTimeoutError:
                    if stop_event.is_set():
                        # update_output("Listening stopped by user.", color="red", size=20)
                        return
                except sr.UnknownValueError:
                    replace_last_line("Could not understand the audio.", color="red", size=20)
                    if stop_event.is_set():
                        return
                except Exception as e:
                    replace_last_line(f"Error: {e}", color="red", size=20)
                    return
    finally:
        is_listening = False
        stop_event.clear()
        # Ensure UI reflects the off state after stopping
        root.after(0, lambda: on_off_button.config(text="OFF"))



def speak(text):
    tts = gTTS(text)
    tts.save('temp.mp3') 

    # Initialize Pygame mixer
    pygame.mixer.init()

    # Load the MP3 file
    pygame.mixer.music.load('temp.mp3')

    # Play the MP3 file
    pygame.mixer.music.play()

    # Keep the program running until the music stops playing
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)
    
    pygame.mixer.music.unload()
    os.remove("temp.mp3") 

def AI(query):
    genai.configure(api_key="AIzaSyAotC4M-yePA_K2mHbNr_1pe3Y-M8pNmSE")
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(query + "\nPlease provide a short reply.")

    return response.text

def processCommand(c):
    try:
        # Show the user input in the output box
        update_output(c, align="right", color="blue",size=20)

        if "open google" in c.lower():
            webbrowser.open("https://google.com")
            update_output("Opening Google...", color="yellow")

        elif "open facebook" in c.lower():
            webbrowser.open("https://facebook.com")
            update_output("Opening Facebook...", color="yellow")

        elif "open youtube" in c.lower():
            webbrowser.open("https://youtube.com")
            update_output("Opening YouTube...", color="yellow")

        elif "open linkedin" in c.lower():
            webbrowser.open("https://linkedin.com")
            update_output("Opening LinkedIn...", color="yellow")

        elif "open website" in c.lower():
            webbrowser.open("https://www.bennett.edu.in/")
            update_output("Opening Bennett University website...", color="yellow")

        elif "open instagram" in c.lower():
            webbrowser.open("https://www.instagram.com/")
            update_output("Opening Instagram...", color="yellow")

        elif "open whatsapp" in c.lower():
            webbrowser.open("https://web.whatsapp.com/")
            update_output("Opening WhatsApp...", color="yellow")

        elif "open twitter" in c.lower():
            webbrowser.open("https://twitter.com/")
            update_output("Opening Twitter...", color="yellow")
    
        elif "open github" in c.lower():
            webbrowser.open("https://github.com/")
            update_output("Opening GitHub...", color="yellow")

        elif "attendance website" in c.lower():
            webbrowser.open("https://student.bennetterp.camu.in/v2/login")
            update_output("Opening Bennett University attendance website...", color="yellow")

    

        elif "news" in c.lower(): 
            entry.delete(0, tk.END)
            news_response = news("f5e28cedb4f54e23a37e762df0e86b92", country="us")
            update_output(news_response)
            # speak(news_response) 

        elif c.lower().startswith("play"):     
            song = c.lower().split(" ")[1]
            link = musicLibrary.music[song]
            webbrowser.open(link)

        else:
            entry.delete(0, tk.END)
            output = AI(c)
            
            update_output(output)
    
    except Exception as e:
        update_output(f"Error: {e}", color="green")
    finally:
        entry.delete(0, tk.END)  # Clear the entry box after task completion


def update_output(text, align="left", color=None, size=15, temp_tag=None):
    label_output.config(state=tk.NORMAL)

    if temp_tag:  # Temporary tag for removable text
        label_output.insert(tk.END, text + "\n", temp_tag)
        label_output.tag_configure(temp_tag, foreground=color, font=("Helvetica", size))
    else:
        label_output.insert(tk.END, text + "\n")
        if color:
            label_output.tag_configure(color, foreground=color, font=("Helvetica", size))
            label_output.tag_add(color, "end-2l", "end-1l")

    if align == "right":
        label_output.tag_configure("right", justify='right')
        label_output.tag_add("right", "end-2l", "end-1l")


    label_output.config(state=tk.DISABLED)

# Define a function for button click
def on_button_click():
    user_input = entry.get()
    threading.Thread(target=processCommand, args=(user_input,)).start()




def on_off_button_toggle():
    global is_listening
    # Ensure the toggle happens only once
    if on_off_button.cget('text') == "OFF":
        on_off_button.config(text='ON')
        is_listening = True
        stop_event.clear()  # Reset the stop_event
        threading.Thread(target=speech_to_text, daemon=True).start()
    else:
        on_off_button.config(text='OFF')
        is_listening = False
        stop_event.set()  # Trigger the stop_event
        label_output.config(state=tk.NORMAL)
        label_output.delete("end-2l", "end-1l")  # Remove "Listening..." text
        label_output.config(state=tk.DISABLED)
        # Process any recognized text if available
        recognized_text_value = recognized_text.get()
        if recognized_text_value:
            threading.Thread(target=processCommand, args=(recognized_text_value,), daemon=True).start()

# Create a frame to hold the entry field and the button
entry_frame = tk.Frame(root , bg='#d4f6f0')
entry_frame.pack(side=tk.BOTTOM, pady=10)

# Add an on/off button to the frame, to the left of the entry field
on_off_button = tk.Button(entry_frame, text="OFF", command=on_off_button_toggle)
on_off_button.pack(side=tk.LEFT)

# Add an entry field to the frame
entry = tk.Entry(entry_frame, width=160,bg='#9691d3')
entry.pack(side=tk.LEFT, ipadx=10, ipady=5)

# add image experiment
send_image = PhotoImage(file=r"send2.png") 

# Add a button to the frame, next to the entry field
button = tk.Button(entry_frame,image=send_image , command=on_button_click)
button.pack(side=tk.RIGHT)

button.image = send_image   # to avoid garbage collection

# Add a label to display the output
label_output = tk.Text(root, wrap=tk.WORD, height=90, width=130,bg='#d4f6f0')
label_output.pack(pady=10)
label_output.config(state=tk.DISABLED)  # Make the text widget read-only

# Initialize the listening state and recognized text
is_listening = False
recognized_text = tk.StringVar()



# Run the Tkinter event loop
root.mainloop()
