import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import os

def get_data_file_path():
    return os.path.join(os.path.dirname(__file__), "../A1 - Resources/studentMarks.txt")

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
