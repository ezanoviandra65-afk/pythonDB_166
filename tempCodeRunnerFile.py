import tkinter as tk
from tkinter import messagebox
import sqlite3
 
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
# LANJUTAN KODE
# ---------------------------------------------------------------
 
def prediksi_fakultas(biologi, fisika, inggris):
    """Tentukan fakultas berdasarkan nilai yang paling tinggi."""
    tertinggi = max(biologi, fisika, inggris)
    hasil = []
 
    if biologi == tertinggi:
        hasil.append("Kedokteran")
    if fisika == tertinggi:
        hasil.append("Teknik")
    if inggris == tertinggi:
        hasil.append("Bahasa")
 
    # Jika ada nilai tertinggi yang sama, gabungkan hasilnya
    return " / ".join(hasil)
 
 
def submit_nilai():
    # 1. Ambil data dari entry
    nama = entry_nama.get().strip()
 
    if nama == "":
        messagebox.showwarning("Peringatan", "Nama siswa harus diisi!")
        return
 
    # 2. Validasi: nilai harus angka bulat 0 - 100
    try:
        biologi = int(entry_biologi.get())
        fisika = int(entry_fisika.get())
        inggris = int(entry_inggris.get())
    except ValueError:
        messagebox.showerror("Error", "Nilai harus berupa angka bulat!")
        return
 
    for nilai in (biologi, fisika, inggris):
        if nilai < 0 or nilai > 100:
            messagebox.showerror("Error", "Nilai harus antara 0 sampai 100!")
            return
 
    # 3. Tentukan prediksi fakultas
    prediksi = prediksi_fakultas(biologi, fisika, inggris)
 
    # 4. Simpan ke database SQLite
    conn = sqlite3.connect("nilai_siswa.db")
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO nilai_siswa (nama_siswa, biologi, fisika, inggris, prediksi_fakultas) "
        "VALUES (?, ?, ?, ?, ?)",
        (nama, biologi, fisika, inggris, prediksi),
    )
    conn.commit()
    conn.close()
 
    # 5. Tampilkan hasil
    label_hasil.config(text=f"Prediksi: {nama} → {prediksi}")
    messagebox.showinfo("Berhasil", f"Data tersimpan.\nPrediksi fakultas: {prediksi}")
 
    # 6. Kosongkan entry
    entry_nama.delete(0, tk.END)
    entry_biologi.delete(0, tk.END)
    entry_fisika.delete(0, tk.END)
    entry_inggris.delete(0, tk.END)
 
 
# ---------------------------------------------------------------
# TAMPILAN (Tkinter)
# ---------------------------------------------------------------
BG = "#2e2f55"
ENTRY_BG = "#7479e8"
PINK = "#ff7ad9"
TOMBOL = "#9a9dfa"
PUTIH = "#ffffff"
GELAP = "#1c1d3a"
 
root = tk.Tk()
root.title("Prediksi Fakultas Siswa")
root.geometry("400x500")
root.configure(bg=BG)
root.resizable(False, False)
 
tk.Label(
    root, text="🎓 Prediksi Fakultas", bg=BG, fg=PINK,
    font=("Segoe UI", 18, "bold"),
).pack(pady=(20, 10))
 
 
def buat_input(teks):
    """Buat satu label + entry, lalu kembalikan entry-nya."""
    tk.Label(
        root, text=teks, bg=BG, fg=PUTIH, font=("Segoe UI", 10, "bold")
    ).pack(pady=(8, 0))
    entry = tk.Entry(
        root, width=32, bg=ENTRY_BG, fg=PUTIH, insertbackground=PUTIH,
        relief="flat", font=("Segoe UI", 10), justify="center",
    )
    entry.pack(ipady=4)
    return entry
 
 
entry_nama = buat_input("Nama Siswa")
entry_biologi = buat_input("Nilai Biologi")
entry_fisika = buat_input("Nilai Fisika")
entry_inggris = buat_input("Nilai Inggris")
 
tk.Button(
    root, text="Submit Nilai", command=submit_nilai, bg=TOMBOL, fg=GELAP,
    activebackground=PINK, relief="flat", width=26,
    font=("Segoe UI", 10, "bold"), cursor="hand2",
).pack(pady=(24, 10), ipady=4)
 
label_hasil = tk.Label(
    root, text="Prediksi: -", bg=BG, fg=PINK, font=("Segoe UI", 12, "bold")
)
label_hasil.pack(pady=10)
 
root.mainloop()
