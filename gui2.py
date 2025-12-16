import tkinter as tk
from tkinter import messagebox
from DateTimeApplications import calculate_age  # import function

def calculate():
    d = day_var.get()
    m = month_var.get()
    y = year_var.get()

    try:
        d = int(d); m = int(m); y = int(y)
    except ValueError:
        messagebox.showerror("Error", "Please enter valid numbers")
        return

    age = calculate_age(d, m, y)
    if age is not None:
        result_label.config(text=f"Your age is: {age}")
    else:
        messagebox.showerror("Error", "Invalid birthdate")

# build GUI
root = tk.Tk()
root.title("Age Calculator")

tk.Label(root, text="Day").grid(row=0, column=0)
tk.Label(root, text="Month").grid(row=0, column=1)
tk.Label(root, text="Year").grid(row=0, column=2)

day_var = tk.StringVar()
month_var = tk.StringVar()
year_var = tk.StringVar()

tk.Entry(root, textvariable=day_var, width=5).grid(row=1, column=0)
tk.Entry(root, textvariable=month_var, width=5).grid(row=1, column=1)
tk.Entry(root, textvariable=year_var, width=8).grid(row=1, column=2)

tk.Button(root, text="Calculate", command=calculate).grid(row=2, column=0, columnspan=3)

result_label = tk.Label(root, text="")
result_label.grid(row=3, column=0, columnspan=3)

root.mainloop()
