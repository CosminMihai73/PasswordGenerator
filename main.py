import random
import string
import tkinter as tk
from tkinter import ttk, messagebox
from ttkthemes import themed_tk
import pyperclip


class PasswordManagerGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Password Manager")

        self.menu_frame = ttk.Frame(self.master)
        self.menu_frame.pack(pady=10)

        self.generate_button = ttk.Button(self.menu_frame, text="Generate Password", command=self.generate_password)
        self.generate_button.grid(row=0, column=0, padx=10)

        self.view_button = ttk.Button(self.menu_frame, text="View Passwords", command=self.view_passwords)
        self.view_button.grid(row=0, column=1, padx=10)

    def generate_password(self):
        generate_window = tk.Toplevel(self.master)
        generate_window.title("Generate Password")

        name_label = ttk.Label(generate_window, text="Name:")
        name_label.grid(row=0, column=0, padx=10, pady=10)
        name_entry = ttk.Entry(generate_window)
        name_entry.grid(row=0, column=1, padx=10, pady=10)

        username_label = ttk.Label(generate_window, text="Username:")
        username_label.grid(row=1, column=0, padx=10, pady=10)
        username_entry = ttk.Entry(generate_window)
        username_entry.grid(row=1, column=1, padx=10, pady=10)

        notes_label = ttk.Label(generate_window, text="Notes:")
        notes_label.grid(row=2, column=0, padx=10, pady=10)
        notes_entry = ttk.Entry(generate_window)
        notes_entry.grid(row=2, column=1, padx=10, pady=10)

        special_chars_var = tk.BooleanVar()
        ttk.Checkbutton(generate_window, text="Include Special Characters", variable=special_chars_var).grid(row=3,
                                                                                                             column=0,
                                                                                                             columnspan=2,
                                                                                                             pady=5)

        generate_button = ttk.Button(generate_window, text="Generate and Save", command=lambda: self.generate_and_save(
            name_entry.get(),
            username_entry.get(),
            notes_entry.get(),
            special_chars_var.get(),
            generate_window
        ))
        generate_button.grid(row=4, column=0, columnspan=2, pady=10)

    def generate_and_save(self, name, username, notes, include_special_chars, window):
        generated_password = self.generate_password_string(include_special_chars, length=20)
        self.save_password(name, username, generated_password, notes)
        window.destroy()

    def generate_password_string(self, include_special_chars, length=12, uppercase=True, lowercase=True, digits=True):
        characters = ''
        if uppercase:
            characters += string.ascii_uppercase
        if lowercase:
            characters += string.ascii_lowercase
        if digits:
            characters += string.digits
        if include_special_chars:
            characters += string.punctuation

        if not characters:
            return None

        password = ''.join(random.choice(characters) for _ in range(length))
        return password

    def save_password(self, name, username, password, notes):
        if name and username and password:
            with open("passwords.txt", 'a') as password_file:
                password_file.write(f"Name: {name}\nUsername: {username}\nPassword: {password}\nNotes: {notes}\n---\n")

    def view_passwords(self):
        view_window = tk.Toplevel(self.master)
        view_window.title("View Passwords")

        search_label = ttk.Label(view_window, text="Search:")
        search_label.grid(row=0, column=0, padx=10, pady=10)
        search_entry = ttk.Entry(view_window)
        search_entry.grid(row=0, column=1, padx=10, pady=10)
        search_button = ttk.Button(view_window, text="Search",
                                   command=lambda: self.search_passwords(search_entry.get(), text_widget))
        search_button.grid(row=0, column=2, padx=10, pady=10)

        text_widget = tk.Text(view_window, height=20, width=80)
        text_widget.grid(row=1, column=0, columnspan=3, padx=10, pady=10)

        delete_button = ttk.Button(view_window, text="Delete Password",
                                   command=lambda: self.delete_password(text_widget))
        delete_button.grid(row=2, column=0, pady=10)

        copy_button = ttk.Button(view_window, text="Copy Password", command=lambda: self.copy_password(text_widget))
        copy_button.grid(row=2, column=1, pady=10)

        with open("passwords.txt", 'r') as password_file:
            current_password = ""
            for line in password_file:
                if line.strip() == '---':
                    text_widget.insert(tk.END, current_password + '\n\n')
                    current_password = ""
                else:
                    current_password += line

        text_widget.insert(tk.END, current_password)  # Adaugă ultimul set de date

    def search_passwords(self, keyword, text_widget):
        text_widget.delete(1.0, tk.END)
        with open("passwords.txt", 'r') as password_file:
            current_password = ""
            for line in password_file:
                if 'Name:' in line or 'Username:' in line or 'Password:' in line or 'Notes:' in line:
                    current_password += line
                elif line.strip() == '---':
                    if keyword.lower() in current_password.lower():
                        text_widget.insert(tk.END, current_password + '\n\n')
                    current_password = ""
        text_widget.insert(tk.END, current_password)  # Adaugă ultimul set de date

    def delete_password(self, text_widget):
        selected_text = text_widget.tag_ranges(tk.SEL)
        if selected_text:
            confirm = messagebox.askyesno("Confirm Deletion", "Are you sure you want to delete this password?")
            if confirm:
                text_widget.delete(selected_text[0], selected_text[1])

    def copy_password(self, text_widget):
        selected_text = text_widget.tag_ranges(tk.SEL)
        if selected_text:
            password_to_copy = text_widget.get(selected_text[0], selected_text[1])
            pyperclip.copy(password_to_copy)


if __name__ == "__main__":
    root = themed_tk.ThemedTk(theme="arc")
    app = PasswordManagerGUI(root)
    root.mainloop()
