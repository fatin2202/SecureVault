import os
import base64
import hashlib
from tkinter import Tk, Label, Button, Entry, StringVar, filedialog, messagebox
from cryptography.fernet import Fernet

selected_file = ""

def create_key(password):
    return base64.urlsafe_b64encode(
        hashlib.sha256(password.encode()).digest()
    )

def choose_file():
    global selected_file
    selected_file = filedialog.askopenfilename()
    if selected_file:
        file_name.set(os.path.basename(selected_file))

def encrypt_file():
    if not selected_file:
        messagebox.showerror("Error", "Please choose a file first.")
        return

    password = password_var.get()
    if len(password) < 8:
        messagebox.showerror("Weak password", "Use at least 8 characters.")
        return

    try:
        key = create_key(password)
        cipher = Fernet(key)

        with open(selected_file, "rb") as file:
            data = file.read()

        encrypted_data = cipher.encrypt(data)
        output_file = selected_file + ".encrypted"

        with open(output_file, "wb") as file:
            file.write(encrypted_data)

        messagebox.showinfo("Success", f"Encrypted file saved as:\n{output_file}")

    except Exception as error:
        messagebox.showerror("Error", str(error))

def decrypt_file():
    if not selected_file:
        messagebox.showerror("Error", "Please choose an encrypted file first.")
        return

    password = password_var.get()

    try:
        key = create_key(password)
        cipher = Fernet(key)

        with open(selected_file, "rb") as file:
            encrypted_data = file.read()

        decrypted_data = cipher.decrypt(encrypted_data)

        if selected_file.endswith(".encrypted"):
            output_file = selected_file.replace(".encrypted", ".decrypted")
        else:
            output_file = selected_file + ".decrypted"

        with open(output_file, "wb") as file:
            file.write(decrypted_data)

        messagebox.showinfo("Success", f"Decrypted file saved as:\n{output_file}")

    except Exception:
        messagebox.showerror("Error", "Wrong password or invalid encrypted file.")

app = Tk()
app.title("SecureVault")
app.geometry("420x250")

file_name = StringVar()
password_var = StringVar()

Label(app, text="SecureVault: File Encryption Tool", font=("Arial", 16, "bold")).pack(pady=15)

Button(app, text="Choose File", command=choose_file).pack(pady=5)
Label(app, textvariable=file_name).pack()

Label(app, text="Enter Password").pack(pady=8)
Entry(app, textvariable=password_var, show="*", width=30).pack()

Button(app, text="Encrypt File", command=encrypt_file).pack(pady=10)
Button(app, text="Decrypt File", command=decrypt_file).pack()

app.mainloop()