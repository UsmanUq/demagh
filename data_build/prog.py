import json
import tkinter as tk
from tkinter import ttk
from pathlib import Path

# Initialize JSON file path
JSON_FILE = "arabic_words.json"

# Load existing data or create new file
def load_data():
    try:
        with open(JSON_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

# Save data to JSON
def save_data(data):
    with open(JSON_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

# GUI Application
class ArabicWordApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Arabic Word Dataset Builder")
        self.data = load_data()
        
        # Create form
        self.create_form()
        
        # Create list view
        self.create_list_view()
        
        # Status bar
        self.status = tk.Label(root, text="Ready", bd=1, relief=tk.SUNKEN, anchor=tk.W)
        self.status.pack(side=tk.BOTTOM, fill=tk.X)

    def create_form(self):
        frame = ttk.LabelFrame(self.root, text="Add New Word")
        frame.pack(padx=10, pady=10, fill=tk.X)
        
        # Form fields
        fields = [
            ("Arabic Word", "arabic_word", "str"),
            ("Word Type", "word_type", "dropdown"),
            ("English Meaning", "english_meaning", "str"),
            ("Urdu Meaning", "urdu_meaning", "str"),
            ("Personal Connotation", "personal_connotation", "str"),
            ("Color", "color", "str"),
            ("Shape", "shape", "str"),
            ("Heaviness (1-5)", "heaviness", "int"),
            ("Sharpness (0-5)", "sharpness", "int"),
            ("Purity (1-5)", "purity", "int"),
            ("Divinity (1-5)", "divinity", "int"),
            ("Earthiness (0-5)", "earthiness", "int"),
            ("Emotion", "emotion", "str")
        ]
        
        self.entries = {}
        for i, (label, field, dtype) in enumerate(fields):
            row = i % 6
            col = i // 6 * 2
            lbl = ttk.Label(frame, text=label)
            lbl.grid(row=row, column=col, padx=5, pady=5, sticky=tk.E)
            
            if dtype == "int":
                entry = ttk.Spinbox(frame, from_=0, to=5, width=5)
            elif dtype == "dropdown":  
                entry = ttk.Combobox(frame, values=["noun", "adjective", "verb"], width=17)        
            else:
                entry = ttk.Entry(frame, width=20)
                
            entry.grid(row=row, column=col+1, padx=5, pady=5, sticky=tk.W)
            self.entries[field] = entry
        
        # Submit button
        btn_frame = ttk.Frame(self.root)
        btn_frame.pack(pady=5)
        ttk.Button(btn_frame, text="Add Word", command=self.add_word).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Clear Form", command=self.clear_form).pack(side=tk.LEFT, padx=5)

    def create_list_view(self):
        frame = ttk.LabelFrame(self.root, text="Existing Words")
        frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
        
        columns = ("id", "arabic_word","word_type", "english_meaning", "color", "shape")
        self.tree = ttk.Treeview(frame, columns=columns, show="headings")
        
        for col in columns:
            self.tree.heading(col, text=col.replace("_", " ").title())
            self.tree.column(col, width=100)
        
        self.tree.pack(fill=tk.BOTH, expand=True)
        self.refresh_list()

    def add_word(self):
        try:
            new_word = {
                "id": len(self.data) + 1,  # Auto-incrementing ID
                "arabic_word": self.entries["arabic_word"].get(),
                "english_meaning": self.entries["english_meaning"].get(),
                "word_type": self.entries["word_type"].get(),  # Add word type
                "urdu_meaning": self.entries["urdu_meaning"].get(),
                "personal_connotation": self.entries["personal_connotation"].get(),
                "color": self.entries["color"].get(),
                "shape": self.entries["shape"].get(),
                "heaviness": int(self.entries["heaviness"].get()),
                "sharpness": int(self.entries["sharpness"].get()),
                "purity": int(self.entries["purity"].get()),
                "divinity": int(self.entries["divinity"].get()),
                "earthiness": int(self.entries["earthiness"].get()),
                "emotion": self.entries["emotion"].get()
            }
            
            self.data.append(new_word)
            save_data(self.data)
            self.refresh_list()
            self.clear_form()
            self.status.config(text=f"Added: {new_word['arabic_word']} (ID: {new_word['id']})")
        except Exception as e:
            self.status.config(text=f"Error: {str(e)}")

    def clear_form(self):
        for entry in self.entries.values():
            if isinstance(entry, ttk.Spinbox):
                entry.set(0)
            else:
                entry.delete(0, tk.END)

    def refresh_list(self):
        self.tree.delete(*self.tree.get_children())
        for word in self.data:
            self.tree.insert("", tk.END, values=(
            word["id"],
            word["arabic_word"],
            word["word_type"],
            word["english_meaning"],
            word.get("color", ""),
            word.get("shape", "")
        ))

if __name__ == "__main__":
    root = tk.Tk()
    app = ArabicWordApp(root)
    root.mainloop()
