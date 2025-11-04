# imports
import tkinter as tk
from tkinter import * 
from tkinter import messagebox
from PIL import ImageTk, Image
import os
import itertools
import pygame
import random 

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
    'music_muted': False,
    'difficulty': None,
    'score': 0
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
    
# stop the bg gif to switch to restaurant
def stop_gif():
    global frames
    frames = []
    
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
        
# separate mute button for when math quiz starts
def toggle_music_for_quiz(button):
    if game_state['music_muted']:
        pygame.mixer.music.set_volume(0.3)
        game_state['music_muted'] = False
        button.config(image=unmuted_icon)
        print("Music unmuted")
    else:
        pygame.mixer.music.set_volume(0)
        game_state['music_muted'] = True
        button.config(image=muted_icon)
        print("Music muted")

# resize image 
def resize_image_keep_aspect(img_path, target_height):
    img = Image.open(img_path)
    w, h = img.size
    ratio = target_height / h
    new_width = int(w * ratio)
    img = img.resize((new_width, target_height), Image.Resampling.LANCZOS)
    return img

#  confirmation to quit
def quit_game():
    confirm = messagebox.askyesno("Quit Game?", "Are you sure you want to quit?")
    if confirm:
        root.quit()
        
# mute label
# mute_btn = tk.Label(root, text="MUTE", font=('Georgia', 16, 'bold'), fg="white",
                    # bg=bg_color, cursor='hand2')
# mute_btn.place(x=900, y=485)
# mute_btn.bind('<Button-1>', lambda e: toggle_music())
# mute_btn.bind('<Enter>', lambda e: mute_btn.config(fg="#E71C1C"))
# mute_btn.bind('<Leave>', lambda e: mute_btn.config(fg="white"))

# load mute/unmute icons
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

# menu
def displayMenu():
    
    # difficulty labels
    easy_label.place(x=50, y=200)
    moderate_label.place(x=50, y=260)
    advanced_label.place(x=50, y=320)
    quit_label.place(x=50, y=380)
    game_state['difficulty'] = None

# hover effects for labels
def on_enter(label):
    label.config(fg="#E71C1C", font=('Georgia', 30, 'bold'))

def on_leave(label):
    label.config(fg='white', font=('Georgia', 28))

# user selects difficulty
def select_difficulty(difficulty):
    game_state['difficulty'] = difficulty
    if difficulty == "QUIT":
        root.quit()
    elif difficulty == "EASY":
        start_easy_level()
    else:
        messagebox.showinfo("Difficulty Selected",
                            f"You selected {difficulty} mode!")
        
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
   
# starting easy level
def start_easy_level():
    # hides initial menu
    easy_label.place_forget()
    moderate_label.place_forget()
    advanced_label.place_forget()
    quit_label.place_forget()
    
    barista_panel_width = 260
    right_panel = tk.Frame(root, bg="black")
    right_panel.place(x=960 - barista_panel_width, y=0, width=barista_panel_width, height=540)
    
    try:
        
        surprised_barista_path = os.path.join(script_dir, "images", "surprised_barista.png")
        normal_barista_path = os.path.join(script_dir, "images", "normal_barista.png")

        target_height = 300
        surprised_img = resize_image_keep_aspect(surprised_barista_path, target_height)
        normal_img = resize_image_keep_aspect(normal_barista_path, target_height)
        
        surprised_barista = ImageTk.PhotoImage(surprised_img)
        normal_barista = ImageTk.PhotoImage(normal_img)
        
    except Exception as e:
        print(f"Error loading barista images: {e}")
        barista_label = None
        
    # barista label (hidden initially)
    barista_label = tk.Label(right_panel, bg="black")
    barista_label.place_forget()

    quiz_mute_btn = tk.Label(
    right_panel,
    image=unmuted_icon if not game_state['music_muted'] else muted_icon,
    cursor='hand2',
    bd=0,
    highlightthickness=0,
    bg="black"
    )
    
    quiz_mute_btn.bind('<Button-1>', lambda e: toggle_music_for_quiz(quiz_mute_btn))
    quiz_mute_btn.place(x=(barista_panel_width - 40)//2, y=360)
    
    right_quit_btn = tk.Label(
    right_panel,
    text="QUIT",
    font=('Georgia', 16, 'bold'),
    fg="white",
    bg="black",
    cursor='hand2'
    )
    
    # right quit button
    right_quit_btn.bind('<Button-1>', lambda e: quit_game())
    right_quit_btn.bind('<Enter>', lambda e: right_quit_btn.config(fg="#E71C1C"))
    right_quit_btn.bind('<Leave>', lambda e: right_quit_btn.config(fg="white"))
    right_quit_btn.place(x=(barista_panel_width - 50)//2, y=410)

    # text box
    text_box_height = 180
    text_box = tk.Frame(root, bg="black", height=text_box_height)
    text_box.place(x=0, y=540 - text_box_height, width=960, height=text_box_height)
    
    # story label
    story_label = tk.Label(
        text_box,
        text="",
        font=("Georgia", 16),
        fg="white",
        bg="black",
        wraplength=900,
        justify="left",
        anchor="w",
        padx=20,
        pady=10
    )
    story_label.place(x=0, y=0, width=960, height=text_box_height)

    # hint label
    hint_label = tk.Label(
        text_box,
        text="Press any key to continue...",
        font=("Georgia", 12, "italic"),
        fg="white",
        bg="black"
    )
    hint_label.place(relx=0.5, rely=0.85, anchor="center")
        
    # restaurant background
    restaurant_path = os.path.join(script_dir, "images", "restaurant.png")
    try:
        restaurant_img = Image.open(restaurant_path).resize((960, 540), Image.Resampling.LANCZOS)
        restaurant_bg = ImageTk.PhotoImage(restaurant_img)
    except Exception as e:
        print(f"Error loading restaurant background: {e}")
        restaurant_bg = None
    
    # story lines for the plot
    story_lines = [
        "It’s raining hard tonight. It's weird though, weather forecast didn't mention anything this morning.",
        "I should’ve brought an umbrella at least. Great.",
        "There’s a small restaurant across the street. Warm light inside, maybe they’re still open?",
        "‘Le Charne’. Must be new...",
        "As I step inside, the smell of wine and something… metallic hits me.",
        "The place feels cozy though! The candlelight, drinks, and soft jazz. The storm fades away outside.",
        "A man behind the counter looks up, startled. His sleeves are damp… is that—?",
        "‘Ah, welcome!’ he smiles too quickly as he notices me stare at his mouth and shirt. ‘Pomegranate juice. Messy fruit eh?’ he chuckles.",
        "‘You’ve come at the perfect time stranger,’ he adds. ‘I’ll serve you a drink and meal on the house...if you can solve a few numerical curiosities.’",
        "He leans in, eyes ruby red with a glimmer. ‘Shall we begin?’"
    ]
    current_line =  0
    
    def start_math_quiz(parent_frame):
        score = 0
        question_number = 0
        max_questions = 10
        attempts = 0
        timer_seconds = 20
        timer_id = None
    
        
         # difficulty ranges
        diff = game_state['difficulty']
        if diff == "EASY":
           min_val, max_val = 1, 9
        elif diff == "MODERATE":
           min_val, max_val = 10, 99
        # advanced
        else:  
           min_val, max_val = 1000, 9999
           
        # Score Label
        score_label = tk.Label(parent_frame, text=f"Score: {score}", font=("Georgia", 14), fg="lightgreen", bg="#1A1A1A")
        score_label.place(relx=0.85, rely=0.05, anchor="center")
           
        # question Label
        question_label = tk.Label(parent_frame, text="", font=("Georgia", 18), fg="#E7CBA9", bg="#1A1A1A")
        question_label.place(relx=0.5, rely=0.3, anchor="center")

        # answer entry widget
        answer_entry = tk.Entry(parent_frame, font=("Georgia", 16))
        answer_entry.place(relx=0.5, rely=0.5, anchor="center")

        # feedback Label
        feedback_label = tk.Label(parent_frame, text="", font=("Georgia", 14), fg="yellow", bg="#1A1A1A")
        feedback_label.place(relx=0.5, rely=0.6, anchor="center")
        
        # timer Label
        timer_label = tk.Label(parent_frame, text=f"Time: {timer_seconds}", font=("Georgia", 14), fg="orange", bg="#1A1A1A")
        timer_label.place(relx=0.5, rely=0.2, anchor="center")
        
        current_question = {}
        
        # random integer
        def randomInt():
            return random.randint(min_val, max_val)

        # random operation
        def decideOperation():
            return random.choice(["+", "-"])

        # timer countdown
        def countdown():
            nonlocal timer_seconds, timer_id
            timer_label.config(text=f"Time: {timer_seconds}")
            if timer_seconds > 0:
               timer_seconds -= 1
               timer_id = parent_frame.after(1000, countdown)
            else:
               feedback_label.config(text=f"Time's up! 0 points")
               parent_frame.after(1000, next_question)

        # displays next question
        def displayProblem():
            nonlocal current_question, attempts, timer_seconds, timer_id
            attempts = 0
            timer_seconds = 20
            if timer_id:
               parent_frame.after_cancel(timer_id)
            countdown()

            num1 = randomInt()
            num2 = randomInt()
            op = decideOperation()
            current_question = {"num1": num1, "num2": num2, "op": op}
            question_label.config(text=f"{num1} {op} {num2} =")
            answer_entry.delete(0, END)
            feedback_label.config(text="")
    # function of starting quiz
    def start_quiz():
        # hides story box
        text_box.place_forget()

        # create quiz frame
        quiz_box_width = 960 - barista_panel_width
        quiz_box_height = 540

        quiz_frame = tk.Frame(root, bg="#1A1A1A", highlightbackground="#B19775", highlightthickness=3)
        quiz_frame.place(x=0, y=0, width=quiz_box_width, height=quiz_box_height)

        welcome_label = tk.Label(
        quiz_frame,
        text="Welcome to Le Charne’s Full Course Math Quiz \n\nSolve quickly to impress the barista!",
        font=("Georgia", 18, "bold"),
        fg="#E7CBA9",
        bg="#1A1A1A",
        wraplength=960-barista_panel_width-40,
        justify="center"
        )
        welcome_label.place(relx=0.5, rely=0.3, anchor="center")

        # placeholder for logic
        start_math_quiz(quiz_frame, quiz_label=welcome_label)
    
    # advancing to next lines
    def next_line(event=None):
        nonlocal current_line
        if current_line < len(story_lines):
            story_label.config(text=story_lines[current_line])
            
            # barista expression change
            if current_line == 6 and surprised_barista:
                barista_label.config(image=surprised_barista)
                barista_label.place(
                    x=(barista_panel_width - surprised_img.width)//2,
                    y=(540 - text_box_height - target_height)//2
                )  
            if current_line == 8 and normal_barista:
                barista_label.config(image=normal_barista)
                barista_label.place(
                    x=(barista_panel_width - surprised_img.width)//2,
                    y=(540 - text_box_height - target_height)//2
                )
                
            # change background when stepping inside
            if current_line == 4 and restaurant_bg:
                stop_gif()  # stop GIF animation
                bg_label.config(image=restaurant_bg)
                bg_label.image = restaurant_bg  
        else:
            root.unbind("<Key>")
            start_quiz()
            
        current_line +=1
            
    root.bind("<Key>", next_line)
    next_line()
    
    
    
# start the main loop
root.mainloop()