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
