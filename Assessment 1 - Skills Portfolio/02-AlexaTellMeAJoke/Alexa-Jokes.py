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
