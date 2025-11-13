# imports
import tkinter as tk
from tkinter import Label, Button
from PIL import Image, ImageTk, ImageSequence
import random
import os

# class for the application
class AlexaJokeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Alexa Joke Teller")
        self.root.geometry("960x540")
        self.root.resizable(False, False)
        self.root.configure(bg="black")
        
        # get directory of the script
        self.script_dir = os.path.dirname(os.path.abspath(__file__))
        
        # load jokes from file
        self.jokes = self.load_jokes()
        self.current_joke = None
        self.current_setup = ""
        self.current_punchline = ""
        self.showing_punchline = False
        # tracking if its the first joke
        self.first_joke = True  
        
        # GIF frames storing
        self.gif_frames = {}
        self.current_gif_label = None
        self.animation_id = None
        self.current_frame_index = 0
        
        # store original button positions
        self.button_positions = {}
        
        # load all GIFs
        self.load_all_gifs()
        
        # show opening animation
        self.show_opening_animation()
    
    def load_jokes(self):
        # load jokes from the randomJokes.txt file
        jokes = []
        try:
            parent_dir = os.path.dirname(self.script_dir)
            file_path = os.path.join(parent_dir, "A1 - Resources", "randomJokes.txt")
            
            print(f"Looking for jokes file at: {file_path}")
            
            with open(file_path, 'r', encoding='utf-8') as file:
                for line in file:
                    line = line.strip()
                    if line and '?' in line:
                        parts = line.split('?', 1)
                        setup = parts[0].strip() + '?'
                        punchline = parts[1].strip()
                        jokes.append((setup, punchline))
            
            print(f"Successfully loaded {len(jokes)} jokes.")
            
        except FileNotFoundError:
            print(f"Error: Could not find randomJokes.txt at {file_path}")
            jokes = [("Why did the chicken cross the road?", "To get to the other side.")]
        except Exception as e:
            print(f"Error loading jokes: {e}")
            jokes = [("Why did the chicken cross the road?", "To get to the other side.")]
            
        return jokes
