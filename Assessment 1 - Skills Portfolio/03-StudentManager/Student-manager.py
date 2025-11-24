import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from PIL import Image, ImageTk
import os

# getting file path of txt file
def get_data_file_path():
    return os.path.join(os.path.dirname(__file__), "../A1 - Resources/studentMarks.txt")

# loading students, reading txt file and splitting accordingly
def load_students():
    path = get_data_file_path()
    students = []
    with open(path, "r") as f:
        lines = [l.strip() for l in f.readlines()]
        n = int(lines[0])
        for line in lines[1:n+1]:
            id_, name, m1, m2, m3, exam = line.split(",")
            m1, m2, m3, exam = map(int, [m1, m2, m3, exam])
            students.append({
                "id": id_,
                "name": name,
                "c1": m1,
                "c2": m2,
                "c3": m3,
                "exam": exam
            })
    return students

# save student information according to category
def save_students(students):
    path = get_data_file_path()
    with open(path, "w") as f:
        f.write(str(len(students)) + "\n")
        for s in students:
            f.write(f"{s['id']},{s['name']},{s['c1']},{s['c2']},{s['c3']},{s['exam']}\n")

# getting percentage an dgrade of student
def get_percentage_and_grade(s):
    total_cw = s['c1'] + s['c2'] + s['c3']
    total = total_cw + s['exam']
    pct = (total / 160) * 100
    grade = (
        "A" if pct >= 70 else
        "B" if pct >= 60 else
        "C" if pct >= 50 else
        "D" if pct >= 40 else
        "F"
    )
    return pct, grade

# class for the student manager main gui
class StudentManagerApp:
    def __init__(self, root):
        # for window characteristics
        self.root = root
        self.root.title("🐰 Student Manager Dashboard")
        self.root.geometry("1100x650")
        self.root.resizable(False, False)
        self.root.configure(bg="#eeccd4")

        self.students = load_students()

        # background image
        bg_path = os.path.join(os.path.dirname(__file__), "images/ui_background.png")
        bg = Image.open(bg_path)
        self.bg_photo = ImageTk.PhotoImage(bg)
        tk.Label(self.root, image=self.bg_photo).place(x=0, y=0, relwidth=1, relheight=1)

        # welcome text for user
        self.welcome_label = tk.Label(
            self.root,
            text="Welcome user, view grades below :>",
            font=("Poppins", 18, "bold"),
            fg="white",
            bg="#eeccd4"
        )
        self.welcome_label.place(x=445, y=186)
