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

        # clickable labels for sidebar 
        start_x, start_y, spacing = 88.5, 156.1, 40
        menu_items = [
            ("View All", self.show_student_cards),
            ("View Individual", self.view_individual),
            ("Highest Score", self.show_highest),
            ("Lowest Score", self.show_lowest),
            ("Sort Records", self.sort_students),
            ("Add Student", self.add_student),
            ("Delete Student", self.delete_student),
            ("Update Record", self.update_student)
        ]

        # hover effect
        for i, (text, cmd) in enumerate(menu_items):
            lbl = tk.Label(
                self.root,
                text=text,
                font=("Poppins", 11, "bold"),
                fg="white",
                bg="#eeccd4",
                cursor="hand2"
            )
            lbl.place(x=start_x, y=start_y + i * spacing)
            lbl.bind("<Enter>", lambda e, lbl=lbl: lbl.config(fg="#9caf88"))
            lbl.bind("<Leave>", lambda e, lbl=lbl: lbl.config(fg="white"))
            lbl.bind("<Button-1>", lambda e, func=cmd: func())

        # area for displaying cards
        self.display_area = tk.Frame(self.root, bg="#eeccd4")
        self.display_area.place(x=305, y=249, width=717, height=312)
        self.show_student_cards()

    # showing student cards
    def show_student_cards(self, subset=None):
        for w in self.display_area.winfo_children():
            w.destroy()

        # scrollbar on right side of card display
        canvas = tk.Canvas(self.display_area, bg="#eeccd4", bd=0, highlightthickness=0)
        scroll_y = ttk.Scrollbar(self.display_area, orient="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand=scroll_y.set)
        scroll_y.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)

        inner = tk.Frame(canvas, bg="#eeccd4")
        inner.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=inner, anchor="nw")

        students_to_show = subset if subset else self.students
        if not students_to_show:
            tk.Label(inner, text="No student data.", bg="#eeccd4",
                     fg="#784848", font=("Poppins", 12, "italic")).pack(pady=20)
            return

        columns = 3
        card_w, card_h = (220, 135)
        pad_x, pad_y = (20, 20)

        def colour_for(pct):
            if pct >= 90:
                return "#b9d6b0"  
            elif pct >= 75:
                return "#d3dcb0"  
            elif pct >= 60:
                return "#f4d8b4"  
            elif pct >= 40:
                return "#f0b5ad"  
            else:
                return "#e09792"  

        for i, s in enumerate(students_to_show):
            pct, grade = get_percentage_and_grade(s)
            col = colour_for(pct)
            r, c = divmod(i, columns)
            card = tk.Frame(
                inner, bg=col, width=card_w, height=card_h,
                highlightbackground="#d1b5b9", highlightthickness=1
            )
            card.grid(row=r, column=c, padx=pad_x, pady=pad_y)
            card.grid_propagate(False)

            tk.Label(card, text=s["name"], bg=col, font=("Poppins", 11, "bold"), fg="#544c4b").pack(anchor="center", pady=(10, 0))
            tk.Label(card, text=f"ID: {s['id']}", bg=col, font=("Poppins", 10), fg="#544c4b").pack(anchor="center")
            tk.Label(card, text=f"Coursework: {s['c1']+s['c2']+s['c3']}/60",
                     bg=col, font=("Poppins", 10), fg="#544c4b").pack(anchor="center")
            tk.Label(card, text=f"Exam: {s['exam']}/100",
                     bg=col, font=("Poppins", 10), fg="#544c4b").pack(anchor="center")
            tk.Label(card, text=f"{pct:.1f}%   Grade: {grade}",
                     bg=col, font=("Poppins", 10, "bold"), fg="#38533d").pack(anchor="center", pady=(3, 0))

    # viewing individual student
    def view_individual(self):
        if not self.students:
            messagebox.showinfo("Empty", "No data to view.")
            return
        q = simpledialog.askstring("View Student", "Enter name or ID:")
        if not q:
            return
        subset = [s for s in self.students if q.lower() in s["name"].lower() or s["id"] == q]
        if subset:
            self.show_student_cards(subset)
        else:
            messagebox.showinfo("Not found", "Student not found.")
