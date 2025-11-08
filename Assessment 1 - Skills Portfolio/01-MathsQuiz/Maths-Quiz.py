# imports
import tkinter as tk
from tkinter import * 
from tkinter import messagebox
from PIL import ImageTk, Image
import os
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

# get folder of the script
script_dir = os.path.dirname(os.path.abspath(__file__))

# quiz state tracking
game_state = {
    'music_muted': False,
    'difficulty': None,
    'score': 0
}

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
    
# load mute/unmute images
unmuted_path = os.path.join(script_dir, "images", "unmuted.png")
muted_path = os.path.join(script_dir, "images", "muted.png")

unmuted_icon = ImageTk.PhotoImage(Image.open(unmuted_path).resize((40, 40)))
muted_icon = ImageTk.PhotoImage(Image.open(muted_path).resize((40, 40)))
    
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
        
mute_btn = tk.Label(root, image=unmuted_icon, cursor="hand2", bg="#000008")
mute_btn.place(x=900, y=480)
mute_btn.bind("<Button-1>", lambda e: toggle_music())
        
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
        
# menu
# menu background colour
bg_color = '#000008'

# labels shown in main menu
easy_label = tk.Label(root, text="EASY", font=('Georgia',28), fg='white', cursor='hand2', bg=bg_color)
moderate_label = tk.Label(root, text="MODERATE", font=('Georgia',28), fg='white', cursor='hand2', bg=bg_color)
advanced_label = tk.Label(root, text="ADVANCED", font=('Georgia',28), fg='white', cursor='hand2', bg=bg_color)
quit_label = tk.Label(root, text="QUIT", font=('Georgia',28), fg='white', cursor='hand2', bg=bg_color)

# hover effect
def on_enter(label):
    label.config(fg="#E71C1C", font=('Georgia',30,'bold'))

def on_leave(label):
    label.config(fg='white', font=('Georgia',28))

# items in menu
menu_items = [
    (easy_label, "EASY"),
    (moderate_label, "MODERATE"),
    (advanced_label, "ADVANCED"),
    (quit_label, "QUIT")
]

for lbl, difficulty in menu_items:
    lbl.bind('<Enter>', lambda e, l=lbl: on_enter(l))
    lbl.bind('<Leave>', lambda e, l=lbl: on_leave(l))
    
def displayMenu():
    easy_label.place(x=50, y=200)
    moderate_label.place(x=50, y=260)
    advanced_label.place(x=50, y=320)
    quit_label.place(x=50, y=380)
    game_state['difficulty'] = None

def hide_menu():
    for lbl in [easy_label, moderate_label, advanced_label, quit_label]:
        lbl.place_forget()
        
def select_difficulty(difficulty):
    if difficulty == "QUIT":
        quit_game()
    else:
        game_state['difficulty'] = difficulty
        hide_menu()
        start_level_story()
        
for lbl, difficulty in menu_items:
    lbl.bind('<Button-1>', lambda e, d=difficulty: select_difficulty(d))      

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

# math quiz function

def start_math_quiz(parent_frame, right_panel, barista_label, normal_barista, bloody_barista):
    score = 0
    question_number = 0
    max_questions = 10
    attempts = 0
    timer_seconds = 20
    timer_id = None

    diff = game_state['difficulty']
    if diff == "EASY":
        min_val, max_val, timer_seconds = 1, 9, 20
    elif diff == "MODERATE":
        min_val, max_val, timer_seconds = 10, 99, 15
    # advanced
    else:
        min_val, max_val, timer_seconds = 100, 999, 10

    # labels
    score_label = tk.Label(parent_frame, text=f"Score: {score}", font=("Georgia", 14),
                           fg="lightgreen", bg="#1A1A1A")
    score_label.place(relx=0.85, rely=0.05, anchor="center")

    question_label = tk.Label(parent_frame, text="", font=("Georgia", 18),
                              fg="#E7CBA9", bg="#1A1A1A")
    question_label.place(relx=0.5, rely=0.3, anchor="center")

    answer_entry = tk.Entry(parent_frame, font=("Georgia", 16))
    answer_entry.place(relx=0.5, rely=0.5, anchor="center")

    feedback_label = tk.Label(parent_frame, text="", font=("Georgia", 14),
                              fg="yellow", bg="#1A1A1A")
    feedback_label.place(relx=0.5, rely=0.6, anchor="center")

    timer_label = tk.Label(parent_frame, text=f"Time: {timer_seconds}",
                           font=("Georgia", 14), fg="orange", bg="#1A1A1A")
    timer_label.place(relx=0.5, rely=0.2, anchor="center")
    
    quit_btn = tk.Button(parent_frame, text="QUIT", font=("Georgia", 12),
                         command=quit_game, bg="red", fg="white")
    quit_btn.place(relx=0.95, rely=0.95, anchor="se")

    mute_quiz_btn = tk.Label(parent_frame, image=unmuted_icon, cursor="hand2", bg="#1A1A1A")
    mute_quiz_btn.place(relx=0.05, rely=0.95, anchor="sw")
    mute_quiz_btn.bind('<Button-1>', lambda e: toggle_music(mute_quiz_btn))

    current_question = {}

    # random integer
    def randomInt(): return random.randint(min_val, max_val)
    
    # decides the operation between addition and subtraction
    def decideOperation(): return random.choice(["+", "-"])

    # function for timer countdown
    def countdown():
        nonlocal timer_seconds, timer_id
        timer_label.config(text=f"Time: {timer_seconds}")
        if timer_seconds > 0:
            timer_seconds -= 1
            timer_id = parent_frame.after(1000, countdown)
        else:
            feedback_label.config(text="Time's up! 0 points")
            parent_frame.after(1000, next_question)

    # function for displaying all the elements when a problem is shown
    def displayProblem():
        nonlocal current_question, attempts, timer_seconds, timer_id
        attempts = 0
        timer_seconds = 20
        if timer_id: parent_frame.after_cancel(timer_id)
        countdown()

        num1, num2, op = randomInt(), randomInt(), decideOperation()
        current_question = {"num1": num1, "num2": num2, "op": op}
        question_label.config(text=f"{num1} {op} {num2} =")
        answer_entry.delete(0, END)
        feedback_label.config(text="")

    # function for answer handling
    def isCorrect(event=None):
        nonlocal score, question_number, attempts, timer_id
        if timer_id: parent_frame.after_cancel(timer_id)
        try:
            user_answer = int(answer_entry.get())
        except ValueError:
            feedback_label.config(text="Enter a valid number!")
            countdown()
            return

        # appointing points according to attempt at problem
        correct_answer = current_question['num1'] + current_question['num2'] if current_question['op'] == "+" else current_question['num1'] - current_question['num2']
        if user_answer == correct_answer:
            points = 10 if attempts == 0 else 5
            score += points
            score_label.config(text=f"Score: {score}")
            feedback_label.config(text=f"Correct! +{points} points")
            parent_frame.after(1000, next_question)
        else:
            if attempts == 0:
                feedback_label.config(text="Wrong! One more try!")
                attempts += 1
                countdown()
            else:
                feedback_label.config(text=f"Wrong again! The answer was {correct_answer}")
                parent_frame.after(1000, next_question)

    # function for next question
    def next_question():
        nonlocal question_number
        question_number += 1
        if question_number < max_questions:
            displayProblem()
        else:
            displayResults()

    # function of displaying results according to score of player
    def displayResults():
        for widget in parent_frame.winfo_children():
            widget.destroy()
        result_frame = tk.Frame(parent_frame, bg="black")
        result_frame.place(x=0, y=0, relwidth=1, relheight=1)
        target_height = 300

        if score >= 90:
            result_text = f"Score: {score}/100\nYou impressed the barista with an 'A'! \n Free meal on the house."
            img_path = os.path.join(script_dir, "images", "steak.jpg")
            barista_label.config(image=normal_barista)
        elif score >= 70:
            result_text = f"Score: {score}/100\nSafe for now... with a 'B'. The barista narrows his eyes."
            img_path = os.path.join(script_dir, "images", "steak.jpg")
            barista_label.config(image=normal_barista)
        elif score >= 50:
            result_text = f"Score: {score}/100\nThe barista frowns with your 'C'… Barely acceptable."
            img_path = os.path.join(script_dir, "images", "poison.jpg")
            barista_label.config(image=normal_barista)
        else:
            result_text = f"Score: {score}/100\nThe barista glares and bares his teeth… You failed with an 'F'!"
            img_path = os.path.join(script_dir, "images", "poison.jpg")
            barista_label.config(image=bloody_barista)

        try:
            result_img = Image.open(img_path).resize((300, 300))
            result_photo = ImageTk.PhotoImage(result_img)
            tk.Label(result_frame, image=result_photo, bg="black").place(relx=0.5, rely=0.4, anchor="center")
            result_frame.image = result_photo
        except: pass

        tk.Label(result_frame, text=result_text, font=("Georgia", 18),
                 fg="#E7CBA9", bg="black", justify="center").place(relx=0.5, rely=0.75, anchor="center")

        tk.Button(result_frame, text="Play Again", font=("Georgia", 14),
                  command=lambda: replay_quiz(parent_frame)).place(relx=0.5, rely=0.9, anchor="center")

    # function of replaying quiz after clicking the play again button
    def replay_quiz(parent_frame):
        for widget in parent_frame.winfo_children():
            widget.destroy()
        start_math_quiz(parent_frame, right_panel, barista_label, normal_barista, bloody_barista)

    answer_entry.bind("<Return>", isCorrect)
    displayProblem()
    answer_entry.focus_set()
    
def start_level_story():
    # barista panel features and place
    barista_panel_width = 260
    right_panel = tk.Frame(root, bg="black")
    right_panel.place(x=960 - barista_panel_width, y=0, width=barista_panel_width, height=540)

    # load barista images
    target_height = 300
    normal_barista_img = resize_image_keep_aspect(os.path.join(script_dir, "images", "normal_barista.png"), target_height)
    normal_barista = ImageTk.PhotoImage(normal_barista_img)
    
    bloody_barista_img = resize_image_keep_aspect(os.path.join(script_dir, "images", "bloody_barista.png"), target_height)
    bloody_barista = ImageTk.PhotoImage(bloody_barista_img)
    
    surprised_barista_img = resize_image_keep_aspect(os.path.join(script_dir, "images", "surprised_barista.png"), target_height)
    surprised_barista = ImageTk.PhotoImage(surprised_barista_img)

    # load restaurant image
    restaurant_bg_img = Image.open(os.path.join(script_dir, "images", "restaurant.png")).resize((960, 540))
    restaurant_bg = ImageTk.PhotoImage(restaurant_bg_img)
    
    bg_label.config(image=restaurant_bg)
    bg_label.image = restaurant_bg
    
    # barista label
    barista_label = tk.Label(right_panel, bg="black")
    barista_label.place_forget()

    # text box for dialogue
    text_box_height = 180
    text_box = tk.Frame(root, bg="black", height=text_box_height)
    text_box.place(x=0, y=540 - text_box_height, width=960, height=text_box_height)
    story_label = tk.Label(text_box, text="", font=("Georgia", 16), fg="white", bg="black",
                           wraplength=900, justify="left", anchor="w", padx=20, pady=10)
    story_label.place(x=0, y=0, width=960, height=text_box_height)

    # story lines
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
    current_line = 0

    # function for starting quiz
    def start_quiz():
        text_box.place_forget()
        quiz_frame = tk.Frame(root, bg="#1A1A1A", highlightbackground="#B19775", highlightthickness=3)
        quiz_frame.place(x=0, y=0, width=960 - barista_panel_width, height=540)
        start_math_quiz(quiz_frame, right_panel, barista_label, normal_barista, bloody_barista)

    # function to start next line
    def next_line(event=None):
        nonlocal current_line
        if current_line < len(story_lines):
            story_label.config(text=story_lines[current_line])
            
            # barista expression changes
            if current_line == 6:
                barista_label.config(image=surprised_barista)
                barista_label.place(x=(barista_panel_width - surprised_barista_img.width)//2,
                                    y=(540 - text_box_height - target_height)//2)
            if current_line == 8:
                barista_label.config(image=normal_barista)
                barista_label.place(x=(barista_panel_width - normal_barista_img.width)//2,
                                    y=(540 - text_box_height - target_height)//2)

            # background change
            if current_line == 4:
                stop_gif()
                bg_label.config(image=restaurant_bg)
                bg_label.image = restaurant_bg
        else:
            root.unbind("<Key>")
            start_quiz()
        current_line += 1

    root.bind("<Key>", next_line)
    next_line()
 
# calling function to display main menu
displayMenu()

root.mainloop()