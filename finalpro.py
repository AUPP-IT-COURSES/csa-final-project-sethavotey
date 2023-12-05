import tkinter as tk
from tkinter import ttk
from datetime import datetime
import json
import os

class HomePage:
    def __init__(self, master, on_get_started_callback):
        window_width = 600
        window_height = 400
        master.geometry(f"{window_width}x{window_height}")
        self.master = master
        self.master.title("Home Page")
        self.master.configure(bg="#ADD8e6")

        self.label = ttk.Label(master, text="Welcome to the Expense Tracker", font=('Helvetica', 14))
        self.label.pack(pady=15)


        self.get_started_button = ttk.Button(master, text="Click Me ><", command=on_get_started_callback)
        self.get_started_button.pack(pady=10)

class ExpenseTrackerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Expense Tracker")
        self.root.configure(bg="#ADD8e6")

        self.expenses = []
        self.load_data()

        self.amount_label = ttk.Label(root, text="Amount:")
        self.amount_entry = ttk.Entry(root)
        self.amount_label.grid(row=0, column=0, padx=5, pady=5)
        self.amount_entry.grid(row=0, column=1, padx=5, pady=5)

        self.category_label = ttk.Label(root, text="Category:")
        self.category_entry = ttk.Entry(root)
        self.category_label.grid(row=1, column=0, padx=5, pady=5)
        self.category_entry.grid(row=1, column=1, padx=5, pady=5)

        self.description_label = ttk.Label(root, text="Description:")
        self.description_entry = ttk.Entry(root)
        self.description_label.grid(row=2, column=0, padx=5, pady=5)
        self.description_entry.grid(row=2, column=1, padx=5, pady=5)

        self.add_button = ttk.Button(root, text="Add Expense", command=self.add_expense)
        self.add_button.grid(row=3, column=0, columnspan=2, pady=10)

        self.view_button = ttk.Button(root, text="View Expenses", command=self.view_expenses)
        self.view_button.grid(row=4, column=0, columnspan=2, pady=10)

    def load_data(self):
        if os.path.exists('expenses.json'):
            with open('expenses.json', 'r') as file:
                self.expenses = json.load(file)

    def save_data(self):
        with open('expenses.json', 'w') as file:
            json.dump(self.expenses, file, indent=2)

    def add_expense(self):
        amount = self.amount_entry.get()
        category = self.category_entry.get()
        description = self.description_entry.get()

        if amount and category:
            expense = {
                'amount': float(amount),
                'category': category,
                'description': description,
                'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
            self.expenses.append(expense)
            self.save_data()
            self.amount_entry.delete(0, tk.END)
            self.category_entry.delete(0, tk.END)
            self.description_entry.delete(0, tk.END)
            print("Expense added successfully.")
        else:
            print("Please enter both amount and category.")

    def view_expenses(self):
        expense_window = tk.Toplevel(self.root)
        expense_window.title("Expenses")

        self.root.configure(bg="#ADD8e6")

        tree = ttk.Treeview(expense_window)
        tree["columns"] = ("Amount", "Category", "Description", "Date")
        tree.heading("Amount", text="Amount")
        tree.heading("Category", text="Category")
        tree.heading("Description", text="Description")
        tree.heading("Date", text="Date")


        for expense in self.expenses:
            tree.insert("", "end", values=(expense['amount'], expense['category'],
                                           expense['description'], expense['date']))

        tree.pack()

def on_get_started_callback():
    root.withdraw()  # Hide the home page
    expense_tracker_root = tk.Tk()
    expense_tracker_root.protocol("WM_DELETE_WINDOW", on_expense_tracker_close)
    expense_tracker = ExpenseTrackerGUI(expense_tracker_root)

def on_expense_tracker_close():
        if root.winfo_exists():
         root.quit()  # Quit the Tkinter application loop when the Expense Tracker window is closed

if __name__ == "__main__":
    root = tk.Tk()
    home_page = HomePage(root, on_get_started_callback)
    root.mainloop()
