import tkinter as tk
from tkinter import simpledialog

def enter_password_to_confirm():
    root = tk.Tk()
    root.withdraw()  # Hide the main Tkinter window

    user_input = simpledialog.askstring("Input", "Please enter your name:", show="*")

    if user_input:
        print(f"User entered: {user_input}")
    else:
        print("User cancelled or entered nothing.")

    root.destroy()

if __name__ == "__main__":
    enter_password_to_confirm()