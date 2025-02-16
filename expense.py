import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt


# Database Setup
def init_db():
    conn = sqlite3.connect("expenses.db")
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS expenses (
                        id INTEGER PRIMARY KEY,
                        date TEXT,
                        category TEXT,
                        amount REAL,
                        description TEXT)''')
    conn.commit()
    conn.close()


# Function to add expense
def add_expense():
    date = date_entry.get()
    category = category_entry.get()
    amount = amount_entry.get()
    description = description_entry.get()

    if not (date and category and amount):
        messagebox.showerror("Error", "All fields except description are required!")
        return

    conn = sqlite3.connect("expenses.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO expenses (date, category, amount, description) VALUES (?, ?, ?, ?)",
                   (date, category, float(amount), description))
    conn.commit()
    conn.close()

    messagebox.showinfo("Success", "Expense Added Successfully!")
    load_expenses()


# Function to load expenses into treeview
def load_expenses():
    for item in tree.get_children():
        tree.delete(item)

    conn = sqlite3.connect("expenses.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM expenses")
    rows = cursor.fetchall()
    conn.close()

    for row in rows:
        tree.insert("", "end", values=row)


# Function to delete selected expense
def delete_expense():
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showerror("Error", "Please select an expense to delete")
        return

    item = tree.item(selected_item)
    expense_id = item['values'][0]

    conn = sqlite3.connect("expenses.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM expenses WHERE id=?", (expense_id,))
    conn.commit()
    conn.close()

    messagebox.showinfo("Deleted", "Expense Deleted Successfully!")
    load_expenses()


# Function to export to CSV
def export_csv():
    conn = sqlite3.connect("expenses.db")
    df = pd.read_sql_query("SELECT * FROM expenses", conn)
    df.to_csv("expenses.csv", index=False)
    conn.close()
    messagebox.showinfo("Exported", "Expenses exported to expenses.csv")


# Function to show expense chart
def show_chart():
    conn = sqlite3.connect("expenses.db")
    df = pd.read_sql_query("SELECT category, SUM(amount) as total FROM expenses GROUP BY category", conn)
    conn.close()

    plt.figure(figsize=(6, 4))
    plt.pie(df['total'], labels=df['category'], autopct='%1.1f%%', startangle=140)
    plt.title("Expense Distribution")
    plt.show()


# GUI Setup
root = tk.Tk()
root.title("Expense Tracker")
root.geometry("700x500")

# UI Elements
tk.Label(root, text="Date (YYYY-MM-DD):").grid(row=0, column=0)
date_entry = tk.Entry(root)
date_entry.grid(row=0, column=1)

tk.Label(root, text="Category:").grid(row=1, column=0)
category_entry = tk.Entry(root)
category_entry.grid(row=1, column=1)

tk.Label(root, text="Amount:").grid(row=2, column=0)
amount_entry = tk.Entry(root)
amount_entry.grid(row=2, column=1)

tk.Label(root, text="Description:").grid(row=3, column=0)
description_entry = tk.Entry(root)
description_entry.grid(row=3, column=1)

# Buttons
tk.Button(root, text="Add Expense", command=add_expense).grid(row=4, column=0)
tk.Button(root, text="Delete Expense", command=delete_expense).grid(row=4, column=1)
tk.Button(root, text="Export CSV", command=export_csv).grid(row=5, column=0)
tk.Button(root, text="Show Chart", command=show_chart).grid(row=5, column=1)

# Expense Table
tree = ttk.Treeview(root, columns=("ID", "Date", "Category", "Amount", "Description"), show="headings")
tree.heading("ID", text="ID")
tree.heading("Date", text="Date")
tree.heading("Category", text="Category")
tree.heading("Amount", text="Amount")
tree.heading("Description", text="Description")
tree.grid(row=6, column=0, columnspan=2)

# Initialize Database
init_db()
load_expenses()

root.mainloop()
