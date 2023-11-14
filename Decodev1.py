import os
import string
import random
import subprocess
from tkinter import Tk, Button, Checkbutton, IntVar, Label, Entry, filedialog, messagebox, PhotoImage, ttk
from pathlib import Path
import pyperclip

def generate_key():
    characters = string.ascii_letters + string.digits + '!@#$%^&*()_-=+,.<>?'
    key = ''.join(random.choice(characters) for _ in range(100))
    return key

def encrypt_decrypt(message, key, operation='encrypt'):
    result = ""
    key_index = 0
    for char in message:
        key_char = key[key_index]
        key_index = (key_index + 1) % len(key)
        if operation == 'encrypt':
            result_char = chr((ord(char) + ord(key_char)) % 128)
        else:  # operation == 'decrypt'
            result_char = chr((ord(char) - ord(key_char) + 128) % 128)
        result += result_char
    return result

def encode():
    file_path = Path(filedialog.askopenfilename())
    if file_path.is_file():
        with file_path.open(mode='r') as file:
            content = file.read()
            key = generate_key()
            encrypted_content = encrypt_decrypt(content, key, 'encrypt')

            encrypted_file_path = file_path.with_name(file_path.stem + '_encrypted.txt')
            with encrypted_file_path.open(mode='w') as encrypted_file:
                encrypted_file.write(encrypted_content)

            pyperclip.copy(key)
            messagebox.showinfo("Success!", "Key copied to clipboard and file encrypted.")

    else:
        messagebox.showerror("Error", "File does not exist.")

def decode():
    file_path = Path(filedialog.askopenfilename())
    if file_path.is_file():
        with file_path.open(mode='r') as file:
            content = file.read()
            key = pyperclip.paste()  # Retrieve the key from the clipboard
            decrypted_content = encrypt_decrypt(content, key, 'decrypt')

            decrypted_file_path = file_path.with_name(file_path.stem + '_decrypted.txt')
            with decrypted_file_path.open(mode='w') as decrypted_file:
                decrypted_file.write(decrypted_content)

            messagebox.showinfo("Success!", "File decrypted.")

    else:
        messagebox.showerror("Error", "File does not exist.")

root = Tk()
root.title("Monkey keyboard encoder/decoder v1")
root.geometry("400x300")

# Set window icon for the taskbar
icon_path = os.path.join(os.path.dirname(__file__), "recurces", "asda.png")
icon_image = PhotoImage(file=icon_path)
root.iconphoto(True, icon_image)

# Set background image
background_path = os.path.join(os.path.dirname(__file__), "recurces", "dadada.png")
background_image = PhotoImage(file=background_path)
background_label = Label(root, image=background_image)
background_label.place(relwidth=1, relheight=1)

toggle_var = IntVar()
toggle_var.set(1)  # Set default to encode

toggle_btn = Checkbutton(root, text="Encode", variable=toggle_var, bg='yellow')
toggle_btn.pack()

encode_btn = Button(root, text="Select File to Encode", command=encode, bg='yellow')
decode_btn = Button(root, text="Select File to Decode", command=decode, bg='yellow')
key_label = Label(root, text="Key:")
key_input = Entry(root)

def toggle():
    if toggle_var.get() == 1:
        decode_btn.pack_forget()
        key_label.pack_forget()
        key_input.pack_forget()
        encode_btn.pack()
    else:
        encode_btn.pack_forget()
        key_label.pack()
        key_input.pack()
        decode_btn.pack()

toggle_btn.config(command=toggle)
toggle()



root.mainloop()
