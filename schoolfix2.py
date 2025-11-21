import json
import os
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext, filedialog
from datetime import datetime
import shutil
import uuid

# ============================================
# KONFIGURASI
# ============================================
DOCUMENTS = os.path.expanduser("~/Documents")
FOLDER = os.path.join(DOCUMENTS, "SchoolFix")
DATA_FILE = os.path.join(FOLDER, "data.json")
BUKTI_FOLDER = os.path.join(FOLDER, "bukti")

os.makedirs(FOLDER, exist_ok=True)
os.makedirs(BUKTI_FOLDER, exist_ok=True)

PASSWORD_GURU = "guru123"  # Ganti kalau mau

# ============================================
# DATABASE
# ============================================
def load_data():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return []
    return []

def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

def new_nomor():
    data = load_data()
    return 1 if not data else max(d["nomor"] for d in data) + 1

# ============================================
# ROOT + SCROLL (SUDAH DIPERBAIKI!)
# ============================================
root = tk.Tk()
root.title("SchoolFix v18.0")
root.geometry("1000x700")
root.configure(bg="#fff8e1")

canvas = tk.Canvas(root, highlightthickness=0, bg="#fff8e1")
scrollbar = ttk.Scrollbar(root, orient="vertical", command=canvas.yview)  # DIPERBAIKI!
scrollable_frame = tk.Frame(canvas, bg="#fff8e1")

scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
canvas.configure(yscrollcommand=scrollbar.set)

canvas.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")

# Scroll dengan mouse
def _on_mousewheel(event):
    canvas.yview_scroll(int(-1*(event.delta/120)), "units")
root.bind_all("<MouseWheel>", _on_mousewheel)

# ============================================
# CORAK BATIK LUCU
# ============================================
def buat_corak_batik():
    for x in range(0, 3000, 100):
        for y in range(0, 3000, 100):
            canvas.create_polygon(x, y+50, x+50, y, x+100, y+50, x+50, y+100, fill="#ff6d00", outline="#d50000", width=3)
            canvas.create_polygon(x+25, y+75, x+75, y+25, x+125, y+75, x+75, y+125, fill="#ffd600", outline="#6a1b9a", width=3)
            canvas.create_oval(x+40, y+40, x+60, y+60, fill="#6a1b9a")
            canvas.create_oval(x+45, y+45, x+55, y+55, fill="white")

buat_corak_batik()

# ============================================
# TOMBOL KELUAR
# ============================================
def tombol_keluar():
    tk.Button(root, text="KELUAR", font=("Arial", 12, "bold"), bg="#ff1744", fg="white", command=root.quit).place(x=20, y=20)

tombol_keluar()

# ============================================
# MENU UTAMA
# ============================================
def menu_utama():
    for w in scrollable_frame.winfo_children():
        w.destroy()

    tk.Label(scrollable_frame, text="🌈 SCHOOLFIX 🌈", font=("Comic Sans MS", 40, "bold"), fg="#d50000", bg="#fff8e1").pack(pady=60)
    tk.Label(scrollable_frame, text="Aplikasi Paling Ceria di Sekolahmu! 😄", font=("Comic Sans MS", 18), fg="#1a237e", bg="#fff8e1").pack(pady=10)

    tk.Button(scrollable_frame, text="LAPOR KERUSAKAN FASILITAS 🛠️", font=("Arial", 16, "bold"), bg="#00e676", fg="white", height=3, width=40,
              command=lambda: form_lapor("fasilitas")).pack(pady=20)

    tk.Button(scrollable_frame, text="LAPOR PELANGGARAN KEDISIPLINAN 🚨", font=("Arial", 16, "bold"), bg="#ff9100", fg="white", height=3, width=40,
              command=lambda: form_lapor("disiplin")).pack(pady=20)

    tk.Button(scrollable_frame, text="DASHBOARD GURU / WAKA ✨", font=("Arial", 16, "bold"), bg="#8a2be2", fg="#ffff00", height=3, width=40,
              command=login_guru).pack(pady=40)

    tk.Label(scrollable_frame, text="v18.0", font=("Comic Sans MS", 14, "bold"), fg="#8a2be2", bg="#fff8e1").pack(pady=50)

# ============================================
# FORM LAPOR
# ============================================
def form_lapor(jenis):
    for w in scrollable_frame.winfo_children():
        w.destroy()

    warna = "#00e676" if jenis == "fasilitas" else "#ff9100"

    tk.Label(scrollable_frame, text="LAPOR " + ("KERUSAKAN FASILITAS 🛠️" if jenis == "fasilitas" else "PELANGGARAN KEDISIPLINAN 🚨"),
             font=("Comic Sans MS", 28, "bold"), fg=warna, bg="#fff8e1").pack(pady=30)

    frame = tk.Frame(scrollable_frame, bg="white", relief="groove", bd=10)
    frame.pack(padx=80, pady=20, fill="both", expand=True)

    tk.Label(frame, text="Nama pelapor (boleh kosong = anonim)", font=("Arial", 12), bg="white").pack(anchor="w", pady=(20,5))
    nama = tk.Entry(frame, font=("Arial", 11), width=60)
    nama.pack(pady=5)

    tk.Label(frame, text="Kelas", font=("Arial", 12), bg="white").pack(anchor="w", pady=(10,5))
    kelas = tk.Entry(frame, font=("Arial", 11), width=60)
    kelas.pack(pady=5)

    pelaku = None
    if jenis == "disiplin":
        tk.Label(frame, text="Nama Pelaku Pelanggaran", font=("Arial", 12), bg="white").pack(anchor="w", pady=(10,5))
        pelaku = tk.Entry(frame, font=("Arial", 11), width=60)
        pelaku.pack(pady=5)

    tk.Label(frame, text="Kategori", font=("Arial", 12), bg="white").pack(anchor="w", pady=(10,5))
    kategori_var = tk.StringVar(value="Meja/Kursi Rusak" if jenis == "fasilitas" else "Terlambat")
    kategori = ttk.Combobox(frame, textvariable=kategori_var, state="readonly", font=("Arial", 11), width=57)
    if jenis == "fasilitas":
        kategori["values"] = ("Meja/Kursi Rusak","Lampu/AC","Pintu/Jendela","Toilet","Proyektor","Papan Tulis","Atap Bocor","Lain-lain")
    else:
        kategori["values"] = ("Terlambat","Boloss","Merokok","Bawa HP","Rambut Panjang","Seragam Tidak Lengkap","Berkelahi","Membully","Vandalisme","Lain-lain")
    kategori.pack(pady=5)

    tk.Label(frame, text="Deskripsi / Kronologi", font=("Arial", 12), bg="white").pack(anchor="w", pady=(10,5))
    deskripsi = scrolledtext.ScrolledText(frame, height=10, font=("Arial", 11))
    deskripsi.pack(pady=5, fill="x")

    foto_list = []

    tk.Label(frame, text="Foto/ Bukti (opsional)", font=("Arial", 12), bg="white").pack(anchor="w", pady=(20,5))
    list_foto = tk.Listbox(frame, height=5)
    list_foto.pack(pady=5, fill="x")

    frame_btn_foto = tk.Frame(frame, bg="white")
    frame_btn_foto.pack(pady=10)
    tk.Button(frame_btn_foto, text="+ Tambah Foto", bg="#00e676", fg="white", command=lambda: [foto_list.append(f) or list_foto.insert(tk.END, os.path.basename(f)) for f in filedialog.askopenfilenames()]).pack(side="left", padx=10)
    tk.Button(frame_btn_foto, text="− Hapus", bg="#ff1744", fg="white", command=lambda: [list_foto.delete(i) or foto_list.pop(i) for i in list_foto.curselection()[::-1]] or None).pack(side="left", padx=10)

    def kirim():
        if not deskripsi.get("1.0","end").strip():
            messagebox.showwarning("Wajib!", "Deskripsi harus diisi ya kak! 😊")
            return

        nomor = new_nomor()
        saved = []
        for i, path in enumerate(foto_list):
            if os.path.exists(path):
                ext = os.path.splitext(path)[1].lower() or ".jpg"
                nama_baru = f"bukti_{nomor}_{i+1}{ext}"
                shutil.copy2(path, os.path.join(BUKTI_FOLDER, nama_baru))
                saved.append(nama_baru)

        laporan = {
            "nomor": nomor,
            "jenis": jenis,
            "nama": nama.get().strip() or "Anonim",
            "kelas": kelas.get().strip() or "-",
            "kategori": kategori_var.get(),
            "deskripsi": deskripsi.get("1.0","end").strip(),
            "pelaku": pelaku.get().strip() if jenis == "disiplin" else "",
            "tanggal": datetime.now().strftime("%d-%m-%Y %H:%M"),
            "status": "Baru",
            "foto": saved
        }

        data = load_data()
        data.append(laporan)
        save_data(data)
        messagebox.showinfo("YEAY! 🎉🎊", f"Laporan #{nomor} berhasil dikirim ke guru!\nGuru pasti senang deh! 😄")
        menu_utama()

    tk.Button(frame, text="KIRIM LAPORAN SEKARANG!", font=("Arial", 20, "bold"), bg=warna, fg="white", height=2, command=kirim).pack(pady=30)

    tk.Button(scrollable_frame, text="Kembali ke Menu", bg="#8a2be2", fg="white", command=menu_utama).pack(pady=10)

# ============================================
# LOGIN GURU
# ============================================
def login_guru():
    win = tk.Toplevel(root)
    win.title("Login Guru")
    win.geometry("450x350")
    win.configure(bg="#fff8e1")
    win.grab_set()
    win.focus_force()

    tk.Label(win, text="PASSWORD GURU", font=("Arial", 20, "bold"), fg="#d50000", bg="#fff8e1").pack(pady=60)

    pass_entry = tk.Entry(win, show="*", font=("Arial", 16), justify="center", width=25)
    pass_entry.pack(pady=10)
    pass_entry.focus_set()

    def cek(event=None):
        if pass_entry.get() == PASSWORD_GURU:
            win.destroy()
            dashboard_guru()
        else:
            messagebox.showerror("Ups!", "Password salah nih guru! 😅")

    tk.Button(win, text="MASUK", font=("Arial", 18, "bold"), bg="#00e676", fg="white", height=2, width=15, command=cek).pack(pady=30)

    win.bind("<Return>", cek)
    pass_entry.bind("<Return>", cek)

# ============================================
# DASHBOARD GURU
# ============================================
def dashboard_guru():
    for w in scrollable_frame.winfo_children():
        w.destroy()

    tk.Label(scrollable_frame, text="DASHBOARD GURU / WAKA ✨", font=("Comic Sans MS", 28, "bold"), fg="#d50000").pack(pady=20)
    tk.Button(scrollable_frame, text="Refresh", bg="#00e676", fg="white", command=dashboard_guru).pack(pady=10)
    tk.Button(scrollable_frame, text="Kembali", bg="#d50000", fg="white", command=menu_utama).pack(pady=5)

    data = load_data()
    if not data:
        tk.Label(scrollable_frame, text="Belum ada laporan nih guru! 😊", font=("Comic Sans MS", 18), fg="gray").pack(pady=100)
        return

    cols = ("No", "Jenis", "Nama", "Kelas", "Kategori", "Status", "Tanggal")
    tree = ttk.Treeview(scrollable_frame, columns=cols, show="headings", height=20)
    for col in cols:
        tree.heading(col, text=col)
        tree.column(col, width=180, anchor="center")
    tree.pack(fill="both", expand=True, padx=50, pady=20)

    for item in sorted(data, key=lambda x: x["nomor"], reverse=True):
        jenis_text = "Fasilitas" if item["jenis"] == "fasilitas" else "Disiplin"
        nama = item.get("nama") or item.get("pelapor", "Anonim")
        kelas = item.get("kelas") or "-"
        tree.insert("", "end", values=(item["nomor"], jenis_text, nama, kelas, item["kategori"], item["status"], item["tanggal"]))

    style = ttk.Style()
    style.configure("Treeview", background="white", fieldbackground="white", rowheight=40, font=("Arial", 10))
    style.configure("Treeview.Heading", background="#d50000", foreground="white")

    tree.tag_configure("Baru", background="#fff3e0")
    tree.tag_configure("Dalam Proses", background="#e3f2fd")
    tree.tag_configure("Selesai", background="#e8f5e8")

    def detail(event):
        sel = tree.selection()
        if not sel: return
        nomor = tree.item(sel[0])["values"][0]
        lap = next(x for x in data if x["nomor"] == nomor)

        det = tk.Toplevel(root)
        det.title(f"Laporan #{nomor}")
        det.geometry("800x600")
        det.configure(bg="#fff8e1")

        info = f"""
LAPORAN #{lap["nomor"]}
JENIS : {'KERUSAKAN FASILITAS 🛠️' if lap["jenis"] == "fasilitas" else "PELANGGARAN KEDISIPLINAN 🚨"}
TANGGAL : {lap["tanggal"]}
STATUS : {lap["status"]}

NAMA : {lap.get("nama") or lap.get("pelapor", "Anonim")}
KELAS : {lap.get("kelas") or "-"}
KATEGORI : {lap["kategori"]}
PELAKU : {lap.get("pelaku", "-")}

DESKRIPSI:
{lap["deskripsi"]}
        """.strip()

        tk.Label(det, text=info, font=("Comic Sans MS", 12), justify="left", bg="white", relief="solid", bd=3).pack(padx=30, pady=30, fill="both", expand=True)

        if lap["foto"]:
            for f in lap["foto"]:
                path = os.path.join(BUKTI_FOLDER, f)
                tk.Button(det, text=f"Buka Bukti {f}", bg="#00e676", fg="white", command=lambda p=path: os.startfile(p)).pack(pady=2)

        def ubah_status(st):
            for d in data:
                if d["nomor"] == nomor:
                    d["status"] = st
            save_data(data)
            messagebox.showinfo("Yeay!", "Status berhasil diubah!")
            det.destroy()
            dashboard_guru()

        frame_btn = tk.Frame(det, bg="#fff8e1")
        frame_btn.pack(pady=20)
        for text, color in [("Baru", "#fb8c00"), ("Dalam Proses", "#3949ab"), ("Selesai", "#43a047")]:
            tk.Button(frame_btn, text=text, bg=color, fg="white", font=("Arial", 12, "bold"), command=lambda t=text: ubah_status(t)).pack(side="left", padx=10)

    tree.bind("<Double-1>", detail)

# ============================================
# JALANKAN
# ============================================
menu_utama()
root.mainloop()