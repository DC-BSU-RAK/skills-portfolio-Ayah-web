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
        self.root.title("Alexa - Joke Assistant")
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
    
    def load_all_gifs(self):
        # load all GIF animations
        gif_files = {
            'opening': 'alexa_opening.gif',
            'listening': 'alexa_listening.gif',
            'loading': 'alexa_loading.gif',
            'speaking': 'alexa_speaking.gif'
        }
        
        gifs_dir = os.path.join(self.script_dir, 'gifs')
        
        for name, filename in gif_files.items():
            try:
                gif_path = os.path.join(gifs_dir, filename)
                print(f"Loading {name} GIF from: {gif_path}")
                
                img = Image.open(gif_path)
                frames = []
                for frame in ImageSequence.Iterator(img):
                    frame = frame.copy()
                    if name == 'opening':
                        frame = frame.resize((960, 540), Image.Resampling.LANCZOS)
                    elif name == 'speaking':
                        # resize speaking gif 
                        frame = frame.resize((200, 200), Image.Resampling.LANCZOS)
                    elif name == 'loading':
                        # get original dimensions
                        orig_width, orig_height = frame.size
                        # calculate aspect ratio
                        aspect_ratio = orig_width / orig_height
                        
                        # target height
                        target_height = 190
                        target_width = int(target_height * aspect_ratio)
                        
                        # resize maintaining aspect ratio
                        frame = frame.resize((target_width, target_height), Image.Resampling.LANCZOS)
                    frames.append(ImageTk.PhotoImage(frame))
                self.gif_frames[name] = frames
                print(f"Successfully loaded {name} GIF with {len(frames)} frames")
                
            except Exception as e:
                print(f"Error loading {name} GIF: {e}")
                self.gif_frames[name] = []
    
    def show_opening_animation(self):
        # show the opening animation once, then switch to main interfac
        self.current_gif_label = Label(self.root, bg="black")
        self.current_gif_label.place(x=0, y=0, width=960, height=540)
        
        self.current_frame_index = 0
        self.play_gif_once('opening', self.create_main_interface)
    
    def play_gif_once(self, gif_name, callback=None):
        # play a GIF animation once and then execute callback
        if gif_name not in self.gif_frames or not self.gif_frames[gif_name]:
            if callback:
                callback()
            return
        
        frames = self.gif_frames[gif_name]
        
        def animate():
            if self.current_frame_index < len(frames):
                self.current_gif_label.configure(image=frames[self.current_frame_index])
                self.current_frame_index += 1
                self.animation_id = self.root.after(50, animate)
            else:
                if callback:
                    callback()
        
        self.current_frame_index = 0
        animate()
    
    def play_gif_loop(self, gif_name):
        # play a GIF animation in a loop
        if self.animation_id:
            self.root.after_cancel(self.animation_id)
        
        if gif_name not in self.gif_frames or not self.gif_frames[gif_name]:
            return
        
        frames = self.gif_frames[gif_name]
        
        def animate():
            if self.current_gif_label:
                frame = frames[self.current_frame_index % len(frames)]
                self.current_gif_label.configure(image=frame)
                self.current_frame_index += 1
                self.animation_id = self.root.after(50, animate)
        
        self.current_frame_index = 0
        animate()
    
    def create_main_interface(self):
        # create main interface with buttons and alexa GIF
        if self.current_gif_label:
            self.current_gif_label.destroy()
        
        # create alexa GIF label 
        self.current_gif_label = Label(self.root, bg="black")
        self.current_gif_label.place(x=480, y=150, anchor="center")
        
        # start with listening animation
        self.play_gif_loop('listening')
        
        # create text label for joke display 
        self.joke_text = Label(
            self.root,
            text="",
            font=("Arial", 14, "bold"),
            bg="black",
            fg="white",
            wraplength=800,
            justify="center"
        )
        self.joke_text.place(x=480, y=320, anchor="center")
        
        # load button images
        self.load_button_images()
        
        # create buttons at the bottom -
        button_y = 480
        
        # button spacing and positioning
        button_spacing = 280
        center_x = 480
        
        # tell me a joke button only shown initially
        joke_x = center_x
        self.joke_button = self.create_button(
            self.joke_button_img,
            lambda: self.button_click_effect(self.joke_button, self.tell_joke),
            joke_x,
            button_y,
            "Alexa tell me a Joke"
        )
        self.button_positions[self.joke_button] = (joke_x, button_y)
        
        # show punchline button 
        punchline_x = center_x - button_spacing // 2
        self.punchline_button = self.create_button(
            self.punchline_button_img,
            lambda: self.button_click_effect(self.punchline_button, self.show_punchline),
            punchline_x,
            button_y,
            "Show Punchline"
        )
        self.button_positions[self.punchline_button] = (punchline_x, button_y)
        self.punchline_button.place_forget()  
        
        # next joke button 
        next_x = center_x + button_spacing // 2
        self.next_button = self.create_button(
            self.next_button_img,
            lambda: self.button_click_effect(self.next_button, self.next_joke),
            next_x,
            button_y,
            "Next Joke"
        )
        self.button_positions[self.next_button] = (next_x, button_y)
        self.next_button.place_forget()  
        
        # quit button 
        quit_x = 880
        quit_y = 50
        self.quit_button = self.create_button(
            self.quit_button_img,
            lambda: self.button_click_effect(self.quit_button, self.root.quit),
            quit_x,
            quit_y,
            "Quit"
        )
        self.button_positions[self.quit_button] = (quit_x, quit_y)
