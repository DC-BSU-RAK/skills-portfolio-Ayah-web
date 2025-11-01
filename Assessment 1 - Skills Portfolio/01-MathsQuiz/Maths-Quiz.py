# imports
import tkinter as tk
from tkinter import * 
from tkinter import messagebox
from PIL import ImageTk, Image
import os
import itertools
import pygame

# init pygame mixer for music
pygame.mixer.init()

# setting up of main menu window
root = Tk()
root.title('Le Charne — Full Course Math Quiz')
root.geometry('960x540')
root.resizable(False, False)
root.configure(bg='#000008')

# quiz state tracking
game_state = {
    'easy_completed': False,
    'medium_completed': False,
    'music_muted': False
}

# get folder of the script
script_dir = os.path.dirname(os.path.abspath(__file__))

# load and play background music
try:
    music_path = os.path.join(script_dir, "music", "bgjazz_music.mp3")
    pygame.mixer.music.load(music_path)
    pygame.mixer.music.set_volume(0.3)
    
    # loops indefinitely
    pygame.mixer.music.play(-1)  
    print("Music loaded successfully")
except Exception as e:
    print(f"Music error: {e}")

# loading gif for main menu
gif_path = os.path.join(script_dir, "gifs", "rainy_night.gif")
frames = []
bg_color = '#000008'

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
bg_label = tk.Label(root, bg='#000008')
bg_label.place(x=0, y=0, relwidth=1, relheight=1) 

# function to make gif play indefinitely
def update_gif(frame_idx=0):

    if frames and len(frames) > 0:
        frame = frames[frame_idx]
        bg_label.config(image=frame)
        bg_label.image = frame  
        root.after(100, update_gif, (frame_idx + 1) % len(frames))
        
# start the animation of gif
if frames:
    update_gif(0)
else:
    print("No frames loaded - check if gif file exists")
    bg_label.config(bg='#000008')
    
# mute button
def toggle_music():
    if game_state['music_muted']:
        pygame.mixer.music.set_volume(0.3)
        game_state['music_muted'] = False
        mute_btn.config(image=unmuted_icon)
        print("Music unmuted")
    else:
        pygame.mixer.music.set_volume(0)
        game_state['music_muted'] = True
        mute_btn.config(image=muted_icon)
        print("Music muted")

# Load mute/unmute icons
try:
    unmuted_path = os.path.join(script_dir, "images", "unmuted.png")
    muted_path = os.path.join(script_dir, "images", "muted.png")
    
    unmuted_img = Image.open(unmuted_path).resize((40, 40), Image.Resampling.LANCZOS)
    unmuted_icon = ImageTk.PhotoImage(unmuted_img)
    
    muted_img = Image.open(muted_path).resize((40, 40), Image.Resampling.LANCZOS)
    muted_icon = ImageTk.PhotoImage(muted_img)
    
    # label for mute button
    mute_btn = tk.Label(
        root,
        image=unmuted_icon,
        cursor='hand2',
        bd=0,
        highlightthickness=0,
        bg=bg_color
    )
    mute_btn.bind('<Button-1>', lambda e: toggle_music())
    mute_btn.place(x=900, y=480)
    
except Exception as e:
    print(f"Error loading mute icons: {e}")

# button click handler
def select_difficulty(difficulty):
    game_state['difficulty'] = difficulty
    print(f"Selected difficulty: {difficulty}")
    
    if difficulty == "QUIT":
        root.quit()
    else:
        messagebox.showinfo("Difficulty Selected", 
                           f"You selected {difficulty} mode!\n\nQuiz functionality will be implemented next!")

# hover effects for labels
def on_enter(label):
    label.config(fg="#E71C1C", font=('Georgia', 30, 'bold'))

def on_leave(label):
    label.config(fg='white', font=('Georgia', 28))

# clickable text labels

# easy label
easy_label = tk.Label(
    root,
    text="EASY",
    font=('Georgia', 28),
    fg='white',
    cursor='hand2',
    bd=0,
    highlightthickness=0,
    bg=bg_color
)
easy_label.place(x=50, y=200)
easy_label.bind('<Button-1>', lambda e: select_difficulty("EASY"))
easy_label.bind('<Enter>', lambda e: on_enter(easy_label))
easy_label.bind('<Leave>', lambda e: on_leave(easy_label))

# moderate label
moderate_label = tk.Label(
    root,
    text="MODERATE",
    font=('Georgia', 28),
    fg='white',
    cursor='hand2',
    bd=0,
    highlightthickness=0,
    bg=bg_color
)
moderate_label.place(x=50, y=260)
moderate_label.bind('<Button-1>', lambda e: select_difficulty("MODERATE"))
moderate_label.bind('<Enter>', lambda e: on_enter(moderate_label))
moderate_label.bind('<Leave>', lambda e: on_leave(moderate_label))

# advanced label
advanced_label = tk.Label(
    root,
    text="ADVANCED",
    font=('Georgia', 28),
    fg='white',
    cursor='hand2',
    bd=0,
    highlightthickness=0,
    bg=bg_color
)
advanced_label.place(x=50, y=320)
advanced_label.bind('<Button-1>', lambda e: select_difficulty("ADVANCED"))
advanced_label.bind('<Enter>', lambda e: on_enter(advanced_label))
advanced_label.bind('<Leave>', lambda e: on_leave(advanced_label))

# quit label
quit_label = tk.Label(
    root,
    text="QUIT",
    font=('Georgia', 28),
    fg='white',
    cursor='hand2',
    bd=0,
    highlightthickness=0,
    bg=bg_color
)
quit_label.place(x=50, y=380)
quit_label.bind('<Button-1>', lambda e: select_difficulty("QUIT"))
quit_label.bind('<Enter>', lambda e: on_enter(quit_label))
quit_label.bind('<Leave>', lambda e: on_leave(quit_label))
    
# start the main loop
root.mainloop()