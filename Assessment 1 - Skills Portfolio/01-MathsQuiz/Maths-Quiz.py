# imports
import tkinter as tk
from tkinter import * 
from PIL import ImageTk, Image
import os
import itertools

# setting up of main menu window
root = Tk()
root.title('Le Charne — Full Course Math Quiz')
root.geometry('960x540')
root.resizable(False, False)

# get folder of the script
script_dir = os.path.dirname(os.path.abspath(__file__))

# loading gif for main menu
gif_path = os.path.join(script_dir, "gifs", "rainy_night.gif")
frames = []

try:
    with Image.open(gif_path) as im:
        frame_index = 0
        while True:
            try:
                frame = ImageTk.PhotoImage(im.copy().resize((960, 540)))
                frames.append(frame)
                frame_index += 1
                im.seek(frame_index)
            except EOFError:
                break
    print(f"Loaded {len(frames)} frames from GIF")
except Exception as e:
    print(f"Error loading GIF: {e}")
    
# creating label for gif
bg_label = tk.Label(root)
bg_label.pack(fill="both", expand=True)

# function to make gif play indefinitely
def update_gif(frame_idx=0):

    if frames and len(frames) > 0:
        frame = frames[frame_idx]
        bg_label.config(image=frame)
        bg_label.image = frame  # Keep reference
        root.after(100, update_gif, (frame_idx + 1) % len(frames))
        
# start the animation of gif
if frames:
    update_gif(0)
else:
    print("No frames loaded - check if gif file exists")
    bg_label.config(bg='#1C0A0A')

# Start the main loop
root.mainloop()