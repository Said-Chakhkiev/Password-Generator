import tkinter as tk
from tkinter import filedialog, messagebox
from googletrans import Translator
import random
import string

class NameTranslatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Password Generator")

        self.translator = Translator()

        self.create_widgets()

    def create_widgets(self):
        self.file_label = tk.Label(self.root, text="Select a file:")
        self.file_label.pack()

        self.file_button = tk.Button(self.root, text="Browse", command=self.load_file)
        self.file_button.pack()

        self.language_label = tk.Label(self.root, text="Select target language:")
        self.language_label.pack()

        self.language_var = tk.StringVar(self.root)
        self.language_var.set("en")  # default value
        self.language_menu = tk.OptionMenu(self.root, self.language_var, "en", "es", "fr", "de", "ru")
        self.language_menu.pack()

        self.password_length_label = tk.Label(self.root, text="Password length:")
        self.password_length_label.pack()

        self.password_length_entry = tk.Entry(self.root)
        self.password_length_entry.insert(0, "5")  # default value
        self.password_length_entry.pack()

        self.password_chars_label = tk.Label(self.root, text="Password characters:")
        self.password_chars_label.pack()

        self.password_chars_var = tk.StringVar(self.root)
        self.password_chars_var.set("letters")  # default value
        self.password_chars_menu = tk.OptionMenu(self.root, self.password_chars_var, "letters", "letters_digits", "all")
        self.password_chars_menu.pack()

        self.process_button = tk.Button(self.root, text="Process", command=self.process_file)
        self.process_button.pack()

    def load_file(self):
        self.filename = filedialog.askopenfilename(filetypes=(("Text files", "*.txt"), ("All files", "*.*")))
        if self.filename:
            self.file_label.config(text=self.filename)

    def generate_password(self, length, chars):
        if chars == "letters":
            chars = string.ascii_letters
        elif chars == "letters_digits":
            chars = string.ascii_letters + string.digits
        elif chars == "all":
            chars = string.ascii_letters + string.digits + string.punctuation
        return ''.join(random.choice(chars) for _ in range(length))

    def process_file(self):
        if not hasattr(self, 'filename'):
            messagebox.showerror("Error", "No file selected")
            return

        target_language = self.language_var.get()
        password_length = int(self.password_length_entry.get())
        password_chars = self.password_chars_var.get()

        output_filename = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=(("Text files", "*.txt"), ("All files", "*.*")))
        if not output_filename:
            return

        with open(self.filename, 'r', encoding='utf-8') as infile, open(output_filename, 'w', encoding='utf-8') as outfile:
            for line in infile:
                name, surname = line.strip().split()
                translated_name = self.translator.translate(name, dest=target_language).text
                translated_surname = self.translator.translate(surname, dest=target_language).text
                password = self.generate_password(password_length, password_chars)
                outfile.write(f"{translated_name} {translated_surname} {password}\n")

        messagebox.showinfo("Success", "Processing complete!")

if __name__ == "__main__":
    root = tk.Tk()
    app = NameTranslatorApp(root)
    root.mainloop()