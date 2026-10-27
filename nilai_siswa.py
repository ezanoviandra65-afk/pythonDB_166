import tkinter as tk
from tkinter import messagebox
import sqlite3
 
# Warna tema
BG = "#2b2d4f"        # latar jendela
ENTRY_BG = "#7c80ea"  # kolom input
TOMBOL = "#8f93f7"    # tombol (kondisi normal)
PINK = "#ff6ec7"      # judul
 
 
# ---------------------------------------------------------------
# DATABASE
# ---------------------------------------------------------------
def create_db():
    conn = sqlite3.connect("nilai_siswa.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS nilai_siswa (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nama_siswa TEXT NOT NULL,
            biologi INTEGER NOT NULL,
            fisika INTEGER NOT NULL,
            inggris INTEGER NOT NULL,
            prediksi_fakultas TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()
 
 
create_db()
 
 
# ---------------------------------------------------------------
# LOGIKA PREDIKSI
# ---------------------------------------------------------------
def prediksi_fakultas(biologi, fisika, inggris):
    if biologi > fisika and biologi > inggris:
        return "Kedokteran"
    elif fisika > biologi and fisika > inggris:
        return "Teknik"
    elif inggris > biologi and inggris > fisika:
        return "Bahasa"
    else:
        return "Tidak Dapat Ditentukan"
 
 
def submit_nilai():
    nama = entry_nama.get().strip()
 
    try:
        bio = int(entry_bio.get())
        fis = int(entry_fis.get())
        ing = int(entry_ing.get())
    except ValueError:
        messagebox.showerror("Error", "Nilai harus berupa angka!")
        return
 
    if not nama:
        messagebox.showerror("Error", "Nama siswa tidak boleh kosong!")
        return
 
    hasil_prediksi = prediksi_fakultas(bio, fis, ing)
 
    conn = sqlite3.connect("nilai_siswa.db")
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO nilai_siswa (nama_siswa, biologi, fisika, inggris, prediksi_fakultas)
        VALUES (?, ?, ?, ?, ?)
    """, (nama, bio, fis, ing, hasil_prediksi))
    conn.commit()
    conn.close()
 
    messagebox.showinfo("Hasil Prediksi", f"Prediksi Fakultas: {hasil_prediksi}")
 
    entry_nama.delete(0, tk.END)
    entry_bio.delete(0, tk.END)
    entry_fis.delete(0, tk.END)
    entry_ing.delete(0, tk.END)
 
 
def on_enter(e):
    btn_submit["bg"] = "#50fa7b"
    btn_submit["fg"] = "black"

def on_leave(e):
    btn_submit["bg"] = TOMBOL
    btn_submit["fg"] = "black"


root = tk.Tk()
root.title("Prediksi Fakultas Siswa")
root.geometry("400x440")
root.configure(bg=BG)
root.resizable(False, False)

tk.Label(
    root, text="🎓 Prediksi Fakultas", bg=BG, fg=PINK,
    font=("Arial", 16, "bold"),
).pack(pady=(20, 15))
