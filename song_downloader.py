import os
import subprocess
import tkinter as tk
from tkinter import filedialog, messagebox

# Default save location
DEFAULT_SAVE_PATH = os.path.expanduser("~/Downloads/TikTok_Audio")

def download_audio(links, save_path):
    """Downloads audio from TikTok links using yt-dlp."""
    os.makedirs(save_path, exist_ok=True)
    for link in links:
        try:
            subprocess.run([
                "yt-dlp",
                "-x", "--audio-format", "mp3",
                "-o", f"{save_path}/%(title)s.%(ext)s",
                link
            ], check=True)
        except subprocess.CalledProcessError as e:
            messagebox.showerror("Error", f"Failed to download: {link}\n{e}")

def browse_save_location():
    """Browse for save location."""
    folder = filedialog.askdirectory(initialdir=DEFAULT_SAVE_PATH, title="Select Save Location")
    if folder:
        save_path_var.set(folder)

def start_download():
    """Start the download process."""
    links = links_text.get("1.0", tk.END).strip().splitlines()
    save_path = save_path_var.get()

    if not links:
        messagebox.showwarning("No Links", "Please paste one or more TikTok links.")
        return

    if not os.path.isdir(save_path):
        messagebox.showwarning("Invalid Path", "Please select a valid save location.")
        return

    download_audio(links, save_path)
    messagebox.showinfo("Download Complete", "All downloads completed!")

# Create the Tkinter window
root = tk.Tk()
root.title("TikTok Audio Downloader")

# Save location
save_path_var = tk.StringVar(value=DEFAULT_SAVE_PATH)

# UI Components
frame = tk.Frame(root, padx=10, pady=10)
frame.pack(fill="both", expand=True)

tk.Label(frame, text="Paste TikTok Links (one per line):").pack(anchor="w", pady=(0, 5))
links_text = tk.Text(frame, height=10, width=50)
links_text.pack(pady=(0, 10))

tk.Label(frame, text="Save Location:").pack(anchor="w", pady=(0, 5))
save_path_entry = tk.Entry(frame, textvariable=save_path_var, width=40)
save_path_entry.pack(side="left", fill="x", expand=True, padx=(0, 5))
browse_button = tk.Button(frame, text="Browse", command=browse_save_location)
browse_button.pack(side="right")

download_button = tk.Button(frame, text="Download", command=start_download, bg="green", fg="white")
download_button.pack(pady=(10, 0))

# Run the application
root.mainloop()
