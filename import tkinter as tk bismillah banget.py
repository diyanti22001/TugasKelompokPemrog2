import tkinter as tk
from tkinter import messagebox
import sqlite3

class FilmReviewApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Aplikasi Review Film")

        self.root.configure(bg='#FFA07A')  # Use your desired color code #E9967A #FFFFFF #FFA07A #B22222

        self.label_judul = tk.Label(root, text="Judul Film:")
        self.label_judul.grid(row=0, column=0, padx=10, pady=10)

        self.entry_judul = tk.Entry(root, width=150)
        self.entry_judul.grid(row=0, column=1, padx=10, pady=10)

        self.label_ulasan = tk.Label(root, text="Ulasan:")
        self.label_ulasan.grid(row=1, column=0, padx=10, pady=10)

        self.entry_ulasan = tk.Text(root, width=100, height=10)
        self.entry_ulasan.grid(row=1, column=1, padx=10, pady=10)

        self.label_rating = tk.Label(root, text="Rating:")
        self.label_rating.grid(row=2, column=0, padx=10, pady=10)

        self.rating_scale = tk.Scale(root, from_=1, to=5, orient=tk.HORIZONTAL, length=200)
        self.rating_scale.grid(row=2, column=1, padx=10, pady=10)

        self.tambah_button = tk.Button(root, text="Tambah Review", command=self.tambah_review)
        self.tambah_button.grid(row=3, column=0, columnspan=2, pady=10)

        self.listbox_reviews = tk.Listbox(root, width=150, height=10)
        self.listbox_reviews.grid(row=4, column=0, columnspan=2, padx=10, pady=10)

        self.load_reviews()
        self.listbox_reviews.bind("<<ListboxSelect>>", self.select_review)

        self.lihat_button = tk.Button(root, text="Lihat Review", command=self.lihat_review)
        self.lihat_button.grid(row=5, column=0, pady=5)

        self.hapus_button = tk.Button(root, text="Hapus Review", command=self.hapus_review)
        self.hapus_button.grid(row=5, column=1, pady=5)

    def tambah_review(self):
        judul = self.entry_judul.get()
        ulasan = self.entry_ulasan.get("1.0", tk.END)
        rating = self.rating_scale.get()

        if judul and ulasan:
            conn = sqlite3.connect("reviews.db")
            cursor = conn.cursor()
            cursor.execute("INSERT INTO reviews (judul, ulasan, rating) VALUES (?, ?, ?)", (judul, ulasan, rating))
            conn.commit()
            conn.close()

            self.entry_judul.delete(0, tk.END)
            self.entry_ulasan.delete("1.0", tk.END)
            self.rating_scale.set(1)
            self.load_reviews()
        else:
            messagebox.showwarning("Peringatan", "Judul dan ulasan harus diisi!")

    def load_reviews(self):
        self.listbox_reviews.delete(0, tk.END)
        conn = sqlite3.connect("reviews.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM reviews")
        reviews = cursor.fetchall()
        conn.close()

        for review in reviews:
            judul = review[1]
            ulasan = review[2]
            rating = review[3]
            self.listbox_reviews.insert(tk.END, f"{judul} - Rating: {rating}")

    def select_review(self, event):
        selected_index = self.listbox_reviews.curselection()
        if selected_index:
            review_info = self.listbox_reviews.get(selected_index[0]).split(" - ")
            judul = review_info[0]
            self.entry_judul.delete(0, tk.END)
            self.entry_judul.insert(tk.END, judul)

    def lihat_review(self):
        selected_index = self.listbox_reviews.curselection()
        if selected_index:
            review_info = self.listbox_reviews.get(selected_index[0]).split(" - ")
            judul = review_info[0]
            conn = sqlite3.connect("reviews.db")
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM reviews WHERE judul=?", (judul,))
            review = cursor.fetchone()
            conn.close()

            messagebox.showinfo("Review", f"Judul: {judul}\nRating: {review[3]}\nUlasan:\n{review[2]}")

    def hapus_review(self):
        selected_index = self.listbox_reviews.curselection()
        if selected_index:
            review_info = self.listbox_reviews.get(selected_index[0]).split(" - ")
            judul = review_info[0]
            conn = sqlite3.connect("reviews.db")
            cursor = conn.cursor()
            cursor.execute("DELETE FROM reviews WHERE judul=?", (judul,))
            conn.commit()
            conn.close()

            self.entry_judul.delete(0, tk.END)
            self.entry_ulasan.delete("1.0", tk.END)
            self.rating_scale.set(1)
            self.load_reviews()

if __name__ == "__main__":
    # Membuat database dan tabel jika belum ada
    conn = sqlite3.connect("reviews.db")
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS reviews (id INTEGER PRIMARY KEY, judul TEXT, ulasan TEXT, rating INTEGER)")
    conn.commit()
    conn.close()

    # Menjalankan aplikasi Tkinter
    root = tk.Tk()
    app = FilmReviewApp(root)
    root.mainloop()
