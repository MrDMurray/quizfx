import pandas as pd
import random
import requests
import pygame
import tkinter as tk
from tkinter import ttk
import os
import time
import glob
import threading

# Initialize pygame mixer for audio playback
pygame.mixer.init()

# Load your CSV file into a pandas DataFrame
def load_csv(filename):
    try:
        data = pd.read_csv(filename, encoding='ISO-8859-1')  # Adjust encoding if necessary
        return data
    except FileNotFoundError:
        print('CSV file not found.')
        return None
    except UnicodeDecodeError:
        print('There was a problem decoding the CSV file. Please check the file encoding.')
        return None

# Generate a filename from the first 3 letters and last 3 letters of the name
def generate_filename(name):
    cleaned_name = name.replace(" ", "").lower()  # Remove spaces and convert to lowercase
    return f"{cleaned_name[:3]}{cleaned_name[-3:]}.mp3"

# Use ElevenLabs API to generate audio files for each name in the CSV
def generate_audio_files(data, api_key, voice_id="onwK4e9ZLuTAKqWW03F9"):
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
    headers = {
        "xi-api-key": api_key,
        "Content-Type": "application/json"
    }
    
    for column in data.columns:
        class_names = data[column].dropna().tolist()  # Get all the names in the column
        for name in class_names:
            filename = generate_filename(name)
            
            # Skip if the file already exists
            if os.path.exists(filename):
                print(f"File {filename} already exists, skipping...")
                continue

            # Data for the ElevenLabs API
            data_payload = {
                "text": name,
                "voice_settings": {
                    "stability": 0.75,
                    "similarity_boost": 0.75
                }
            }
            response = requests.post(url, headers=headers, json=data_payload)

            if response.status_code == 200:
                # Write the MP3 data to file
                with open(filename, 'wb') as f:
                    f.write(response.content)
                print(f'Success! Created {filename}.')
            else:
                print(f'Error: {response.status_code}, {response.text}')

# Play the corresponding MP3 file for the selected student
def play_audio_for_name(name):
    filename = generate_filename(name)
    if os.path.exists(filename):
        # Play the MP3 file using pygame.mixer
        pygame.mixer.music.load(filename)
        pygame.mixer.music.play()

        # Wait for the sound to finish playing
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)  # Keep the script alive while playing
        print(f'Played {filename}.')
    else:
        print(f'File {filename} not found.')

# Function to play the selected music file asynchronously
def play_selected_music():
    selected_music = music_dropdown.get()
    if selected_music and os.path.exists(selected_music):
        # Stop any existing music
        if pygame.mixer.music.get_busy():
            pygame.mixer.music.stop()

        # Play the selected music in a separate thread
        threading.Thread(target=play_music_in_background, args=(selected_music,), daemon=True).start()
    else:
        print(f'Music file {selected_music} not found.')

# Function to actually play music in the background thread
def play_music_in_background(selected_music):
    pygame.mixer.music.load(selected_music)
    pygame.mixer.music.play(-1)  # Loop indefinitely until manually stopped
    print(f'Playing {selected_music} in the background.')

# Function to play a random audience clap sound
def play_random_clap():
    clap_files = load_clap_files()
    if clap_files:
        selected_clap = random.choice(clap_files)
        print(f'Playing random clap: {selected_clap}')
        pygame.mixer.Sound(selected_clap).play()
    else:
        print("No clap sounds found.")

# Function to play a random wrong answer sound
def play_random_wrong_answer():
    wrong_files = load_wrong_answer_files()
    if wrong_files:
        selected_wrong = random.choice(wrong_files)
        print(f'Playing random wrong answer: {selected_wrong}')
        pygame.mixer.music.load(selected_wrong)
        pygame.mixer.music.play()
    else:
        print("No wrong answer sounds found.")

# Function to handle the class selection and playing the student's audio file
def handle_class_selection():
    selected_class = class_dropdown.get()
    if selected_class:
        name = choose_random_name(data, selected_class)
        if name:
            print(f'Playing audio for: {name}')
            play_audio_for_name(name)
        else:
            print(f'No names found in the selected class: {selected_class}')

# Choose a random name from the selected class (column)
def choose_random_name(data, selected_class):
    if selected_class in data.columns:
        class_names = data[selected_class].dropna().tolist()  # Drop any NaN values (empty rows)
        return random.choice(class_names) if class_names else None
    else:
        print(f'Class "{selected_class}" not found in CSV.')
        return None

# Function to handle audio data generation for all names in the CSV
def update_audio_data():
    generate_audio_files(data, api_key)

# Function to dynamically load music files (e.g., "music1.mp3", "music2.mp3")
def load_music_files():
    music_files = glob.glob("music*.mp3")
    return music_files if music_files else []

# Function to dynamically load clap files (e.g., "clap1.wav", "clap2.wav")
def load_clap_files():
    clap_files = glob.glob("clap*.wav")
    return clap_files if clap_files else []

# Function to dynamically load wrong answer files (e.g., "wrong1.mp3", "wrong2.mp3")
def load_wrong_answer_files():
    wrong_files = glob.glob("wrong*.wav")
    return wrong_files if wrong_files else []

# Main function for creating the GUI
def main():
    global data, api_key, class_dropdown, music_dropdown
    
    # Set your API key here
    api_key = '7a8a2f5ba0eec71146fcd9bb848199f2'  # Replace with your ElevenLabs API key
    filename = 'classLists.csv'  # Path to your CSV file
    
    data = load_csv(filename)
    if data is not None:
        # Create the main window
        root = tk.Tk()
        root.title("Class Selector and Music Player")
        
        # Label for the class dropdown
        label_class = tk.Label(root, text="Select a class:")
        label_class.pack(pady=10)
        
        # Create a dropdown menu with the columns (class names) from the CSV
        class_dropdown = ttk.Combobox(root, values=list(data.columns))
        class_dropdown.pack(pady=10)
        
        # Button to select and play a random student's name
        read_button = tk.Button(root, text="Read Random Name", command=handle_class_selection)
        read_button.pack(pady=10)

        # Button to update audio data for all names
        update_button = tk.Button(root, text="Update Audio Data", command=update_audio_data)
        update_button.pack(pady=10)
        
        # Label for the music dropdown
        label_music = tk.Label(root, text="Select music:")
        label_music.pack(pady=10)
        
        # Load available music files
        music_files = load_music_files()
        
        # Create a dropdown menu with the available music files
        music_dropdown = ttk.Combobox(root, values=music_files)
        music_dropdown.pack(pady=10)
        
        # Button to play the selected music file asynchronously
        play_music_button = tk.Button(root, text="Play Selected Music", command=play_selected_music)
        play_music_button.pack(pady=10)

        # Button to play a random clap sound
        play_clap_button = tk.Button(root, text="Play Random Clap", command=play_random_clap)
        play_clap_button.pack(pady=10)

        # Button to play a random wrong answer sound
        play_wrong_button = tk.Button(root, text="Play Wrong Answer", command=play_random_wrong_answer)
        play_wrong_button.pack(pady=10)

        # Start the GUI event loop
        root.mainloop()

if __name__ == '__main__':
    main()
