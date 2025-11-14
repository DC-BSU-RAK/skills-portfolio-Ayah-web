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
    
    def load_button_images(self):
        # load button images
        images_dir = os.path.join(self.script_dir, 'images')
        
        try:
            joke_path = os.path.join(images_dir, 'joke_button.png')
            punchline_path = os.path.join(images_dir, 'punchline_button.png')
            next_path = os.path.join(images_dir, 'next_joke_button.png')
            quit_path = os.path.join(images_dir, 'quit_button.png')
            
            print(f"Loading button images from: {images_dir}")
            
            self.joke_button_img = ImageTk.PhotoImage(Image.open(joke_path))
            self.punchline_button_img = ImageTk.PhotoImage(Image.open(punchline_path))
            self.next_button_img = ImageTk.PhotoImage(Image.open(next_path))
            self.quit_button_img = ImageTk.PhotoImage(Image.open(quit_path))
            
            print("Successfully loaded all button images!")
            
        except Exception as e:
            print(f"Error loading button images: {e}")
            self.joke_button_img = None
            self.punchline_button_img = None
            self.next_button_img = None
            self.quit_button_img = None
    
    def create_button(self, image, command, x, y, text=""):
        # create a button with image or text fallback
        if image:
            button = Button(
                self.root,
                image=image,
                command=command,
                bd=0,
                bg="black",
                activebackground="black",
                relief="flat",
                highlightthickness=0
            )
        else:
            button = Button(
                self.root,
                text=text,
                command=command,
                bg="#1E90FF",
                fg="white",
                font=("Arial", 12, "bold"),
                relief="raised",
                padx=20,
                pady=10
            )
        button.place(x=x, y=y, anchor="center")
        return button
    
    def button_click_effect(self, button, callback):
        # create a button click effect with scale animation
        # get original position from stored positions
        if button not in self.button_positions:
            return
        
        original_x, original_y = self.button_positions[button]
        
        # scale down effect 
        def scale_down():
            current_width = button.winfo_width()
            current_height = button.winfo_height()
            
            # reduce size by 10%
            new_width = int(current_width * 0.9)
            new_height = int(current_height * 0.9)
            
            # update button configuration to appear smaller
            button.config(width=new_width, height=new_height, compound="center")
            
            # schedule scale up after 50ms
            self.root.after(50, scale_up)
        
        # scale up effect (return to normal)
        def scale_up():
            # reset button to normal state
            button.config(width=0, height=0)  
            
            # ensure button is at correct position
            button.place(x=original_x, y=original_y, anchor="center")
            
            # execute callback
            callback()
        
        # start animation
        scale_down()
    
    def tell_joke(self):
        # tell a random joke
        if not self.jokes:
            self.joke_text.config(text="No jokes available!")
            return
        
        # select random joke
        self.current_joke = random.choice(self.jokes)
        self.current_setup, self.current_punchline = self.current_joke
        self.showing_punchline = False
        
        # clear text
        self.joke_text.config(text="")
        
        # change to loading animation
        self.play_gif_loop('loading')
        
        # hide "Tell me a joke" button after first use
        if self.first_joke:
            self.first_joke = False
            self.joke_button.place_forget()
        
        # after a delay, show the setup
        self.root.after(1500, self.display_setup)
    
    def display_setup(self):
        # display the joke setup
        # change to speaking animation
        self.play_gif_loop('speaking')
        
        # show the setup
        self.joke_text.config(text=self.current_setup)
        
        # show punchline and next joke buttons
        punchline_x, punchline_y = self.button_positions[self.punchline_button]
        next_x, next_y = self.button_positions[self.next_button]
        
        self.punchline_button.place(x=punchline_x, y=punchline_y, anchor="center")
        self.punchline_button.config(state="normal")
        
        self.next_button.place(x=next_x, y=next_y, anchor="center")
        self.next_button.config(state="disabled")
    
    def show_punchline(self):
        # Show the punchline
        if not self.showing_punchline:
            self.showing_punchline = True
            
            # add punchline to the display
            full_text = f"{self.current_setup}\n\n{self.current_punchline}"
            self.joke_text.config(text=full_text)
            
            # enable next joke button, disable punchline button
            self.punchline_button.config(state="disabled")
            self.next_button.config(state="normal")
    
    def next_joke(self):
        # tell the next joke
        if not self.jokes:
            self.joke_text.config(text="No jokes available!")
            return
        
        # select random joke
        self.current_joke = random.choice(self.jokes)
        self.current_setup, self.current_punchline = self.current_joke
        self.showing_punchline = False
        
        # clear text
        self.joke_text.config(text="")
        
        # change to loading animation
        self.play_gif_loop('loading')
        
        # sisable next button temporarily
        self.next_button.config(state="disabled")
        
        # after a brief delay, show the setup
        self.root.after(1500, self.display_setup)

if __name__ == "__main__":
    root = tk.Tk()
    app = AlexaJokeApp(root)
    root.mainloop()