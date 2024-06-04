import tkinter as tk
from tkinter import ttk
import sqlite3

def initialize_db():
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            value TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

class DataApp:
    def __init__(self, root):
        self.root = root
        self.page = 1
        self.items_per_page = 10
        self.create_widgets()
        self.load_data()

    def create_widgets(self):
        self.data_frame = ttk.Frame(self.root)
        self.data_frame.pack(fill=tk.BOTH, expand=True)

        self.columns = ('ID', 'Name', 'Value')
        self.tree = ttk.Treeview(self.data_frame, columns=self.columns, show='headings')
        for col in self.columns:
            self.tree.heading(col, text=col)
        self.tree.pack(fill=tk.BOTH, expand=True)

        self.pagination_frame = ttk.Frame(self.root)
        self.pagination_frame.pack(fill=tk.X)

        ttk.Label(self.pagination_frame, text="Items per page:").pack(side=tk.LEFT)
        self.items_per_page_var = tk.StringVar(value=str(self.items_per_page))
        ttk.Entry(self.pagination_frame, textvariable=self.items_per_page_var, width=5).pack(side=tk.LEFT)
        ttk.Button(self.pagination_frame, text="Previous", command=self.prev_page).pack(side=tk.LEFT)
        ttk.Button(self.pagination_frame, text="Next", command=self.next_page).pack(side=tk.LEFT)

        self.search_frame = ttk.Frame(self.root)
        self.search_frame.pack(fill=tk.X)

        ttk.Label(self.search_frame, text="Search:").pack(side=tk.LEFT)
        self.search_term_var = tk.StringVar()
        ttk.Entry(self.search_frame, textvariable=self.search_term_var).pack(side=tk.LEFT)
        ttk.Button(self.search_frame, text="Search", command=self.search_data).pack(side=tk.LEFT)

        self.action_frame = ttk.Frame(self.root)
        self.action_frame.pack(fill=tk.X)

        ttk.Button(self.action_frame, text="Add", command=self.add_data).pack(side=tk.LEFT)
        ttk.Button(self.action_frame, text="Delete", command=self.delete_data).pack(side=tk.LEFT)

    def load_data(self):
        self.tree.delete(*self.tree.get_children())
        conn = sqlite3.connect('data.db')
        cursor = conn.cursor()

        query = "SELECT * FROM data LIMIT ? OFFSET ?"
        cursor.execute(query, (self.items_per_page, (self.page - 1) * self.items_per_page))
        for row in cursor.fetchall():
            self.tree.insert('', 'end', values=row)

        conn.close()

    def prev_page(self):
        if self.page > 1:
            self.page -= 1
            self.load_data()

    def next_page(self):
        self.page += 1
        self.load_data()

    def search_data(self):
        term = self.search_term_var.get()
        self.tree.delete(*self.tree.get_children())
        conn = sqlite3.connect('data.db')
        cursor = conn.cursor()

        query = "SELECT * FROM data WHERE name LIKE ? OR value LIKE ?"
        cursor.execute(query, (f'%{term}%', f'%{term}%'))
        for row in cursor.fetchall():
            self.tree.insert('', 'end', values=row)

        conn.close()

    def add_data(self):
        def save_data():
            name = name_var.get()
            value = value_var.get()
            conn = sqlite3.connect('data.db')
            cursor = conn.cursor()
            cursor.execute("INSERT INTO data (name, value) VALUES (?, ?)", (name, value))
            conn.commit()
            conn.close()
            self.load_data()
            add_window.destroy()

        add_window = tk.Toplevel(self.root)
        add_window.title("Add Data")
        add_window.geometry("300x200")

        ttk.Label(add_window, text="Name:").pack(pady=5)
        name_var = tk.StringVar()
        ttk.Entry(add_window, textvariable=name_var).pack(pady=5)

        ttk.Label(add_window, text="Value:").pack(pady=5)
        value_var = tk.StringVar()
        ttk.Entry(add_window, textvariable=value_var).pack(pady=5)

        ttk.Button(add_window, text="Save", command=save_data).pack(pady=10)

    def delete_data(self):
        selected_item = self.tree.selection()[0]
        id = self.tree.item(selected_item)['values'][0]
        conn = sqlite3.connect('data.db')
        cursor = conn.cursor()
        cursor.execute("DELETE FROM data WHERE id=?", (id,))
        conn.commit()
        conn.close()
        self.load_data()

def main():
    initialize_db()
    app = tk.Tk()
    app.title("Data Management App")

    # Set ttkbootstrap theme
    style = ttk.Style()
    style.theme_use("clam")  # You can change this to any ttkbootstrap theme

    DataApp(app)
    app.mainloop()

if __name__ == "__main__":
    main()
