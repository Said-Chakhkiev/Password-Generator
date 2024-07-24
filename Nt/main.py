import tkinter as tk
from tkinter import filedialog, messagebox
from googletrans import Translator
import random
import string
import json
import pandas as pd

class NameTranslatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Password Generator")
        self.root.geometry("600x400")  
        self.root.configure(bg="#eef4fa")  

        self.translator = Translator()

        self.create_widgets()

    def create_widgets(self):
        frame = tk.Frame(self.root, bg="#eef4fa")
        frame.pack(pady=20)

        self.file_label = tk.Label(frame, text="Select a file:", bg="#eef4fa", fg="#333333", font=("Arial", 14, "bold"))
        self.file_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")

        self.file_button = tk.Button(frame, text="Browse", command=self.load_file, bg="#5d8aa8", fg="black", font=("Arial", 14, "bold"))
        self.file_button.grid(row=0, column=1, padx=10, pady=10)

        self.language_label = tk.Label(frame, text="Select target language:", bg="#eef4fa", fg="#333333", font=("Arial", 14, "bold"))
        self.language_label.grid(row=1, column=0, padx=10, pady=10, sticky="w")

        self.language_var = tk.StringVar(self.root)
        self.language_var.set("en")  
        self.language_menu = tk.OptionMenu(frame, self.language_var, "en", "es", "fr", "de", "ru")
        self.language_menu.config(bg="#5d8aa8", fg="white", font=("Arial", 14, "bold"))
        self.language_menu["menu"].config(bg="#5d8aa8", fg="white", font=("Arial", 14, "bold"))
        self.language_menu.grid(row=1, column=1, padx=10, pady=10)

        self.password_length_label = tk.Label(frame, text="Password length:", bg="#eef4fa", fg="#333333", font=("Arial", 14, "bold"))
        self.password_length_label.grid(row=2, column=0, padx=10, pady=10, sticky="w")

        self.password_length_entry = tk.Entry(frame, font=("Arial", 14))
        self.password_length_entry.insert(0, "5") 
        self.password_length_entry.grid(row=2, column=1, padx=10, pady=10)

        self.password_chars_label = tk.Label(frame, text="Password characters:", bg="#eef4fa", fg="#333333", font=("Arial", 14, "bold"))
        self.password_chars_label.grid(row=3, column=0, padx=10, pady=10, sticky="w")

        self.password_chars_var = tk.StringVar(self.root)
        self.password_chars_var.set("letters")  
        self.password_chars_menu = tk.OptionMenu(frame, self.password_chars_var, "letters", "letters_digits", "all")
        self.password_chars_menu.config(bg="#5d8aa8", fg="white", font=("Arial", 14, "bold"))
        self.password_chars_menu["menu"].config(bg="#5d8aa8", fg="white", font=("Arial", 14, "bold"))
        self.password_chars_menu.grid(row=3, column=1, padx=10, pady=10)

        self.output_format_label = tk.Label(frame, text="Select output format:", bg="#eef4fa", fg="#333333", font=("Arial", 14, "bold"))
        self.output_format_label.grid(row=4, column=0, padx=10, pady=10, sticky="w")

        self.output_format_var = tk.StringVar(self.root)
        self.output_format_var.set("txt") 
        self.output_format_menu = tk.OptionMenu(frame, self.output_format_var, "txt", "json", "xlsx")
        self.output_format_menu.config(bg="#5d8aa8", fg="white", font=("Arial", 14, "bold"))
        self.output_format_menu["menu"].config(bg="#5d8aa8", fg="white", font=("Arial", 14, "bold"))
        self.output_format_menu.grid(row=4, column=1, padx=10, pady=10)

        self.process_button = tk.Button(frame, text="Process", command=self.process_file, bg="#4caf50", fg="black", font=("Arial", 14, "bold"))
        self.process_button.grid(row=5, column=0, columnspan=2, padx=10, pady=20)

    def load_file(self):
        self.filename = filedialog.askopenfilename(filetypes=(("All files", "*.*"),))
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
        output_format = self.output_format_var.get()

        output_filename = filedialog.asksaveasfilename(defaultextension=f".{output_format}", filetypes=(("All files", "*.*"),))
        if not output_filename:
            return

        if not output_filename.endswith(f".{output_format}"):
            output_filename += f".{output_format}"

        if self.filename.endswith('.json'):
            data = self.process_json_file(target_language, password_length, password_chars)
        elif self.filename.endswith('.xlsx'):
            data = self.process_excel_file(target_language, password_length, password_chars)
        else:
            data = self.process_text_file(target_language, password_length, password_chars)

        if output_format == 'txt':
            self.save_as_text(data, output_filename)
        elif output_format == 'json':
            self.save_as_json(data, output_filename)
        elif output_format == 'xlsx':
            self.save_as_excel(data, output_filename)

        messagebox.showinfo("Success", "Processing complete!")

    def process_text_file(self, target_language, password_length, password_chars):
        data = []
        with open(self.filename, 'r', encoding='utf-8') as infile:
            for line in infile:
                name, surname = line.strip().split()
                translated_name = self.translator.translate(name, dest=target_language).text
                translated_surname = self.translator.translate(surname, dest=target_language).text
                password = self.generate_password(password_length, password_chars)
                data.append((translated_name, translated_surname, password))
        return data

    def process_json_file(self, target_language, password_length, password_chars):
        data = []
        with open(self.filename, 'r', encoding='utf-8') as infile:
            json_data = json.load(infile)
            for item in json_data:
                name = item['name']
                surname = item['surname']
                translated_name = self.translator.translate(name, dest=target_language).text
                translated_surname = self.translator.translate(surname, dest=target_language).text
                password = self.generate_password(password_length, password_chars)
                data.append((translated_name, translated_surname, password))
        return data

    def process_excel_file(self, target_language, password_length, password_chars):
        data = []
        df = pd.read_excel(self.filename)
        for index, row in df.iterrows():
            name = row['name']
            surname = row['surname']
            translated_name = self.translator.translate(name, dest=target_language).text
            translated_surname = self.translator.translate(surname, dest=target_language).text
            password = self.generate_password(password_length, password_chars)
            data.append((translated_name, translated_surname, password))
        return data

    def save_as_text(self, data, output_filename):
        with open(output_filename, 'w', encoding='utf-8') as outfile:
            for item in data:
                outfile.write(f"{item[0]} {item[1]} {item[2]}\n")

    def save_as_json(self, data, output_filename):
        json_data = [{'name': item[0], 'surname': item[1], 'password': item[2]} for item in data]
        with open(output_filename, 'w', encoding='utf-8') as outfile:
            json.dump(json_data, outfile, ensure_ascii=False, indent=4)

    def save_as_excel(self, data, output_filename):
        df = pd.DataFrame(data, columns=['name', 'surname', 'password'])
        df.to_excel(output_filename, index=False)

if __name__ == "__main__":
    root = tk.Tk()
    app = NameTranslatorApp(root)
    root.mainloop()
