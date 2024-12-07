import csv
import os
import subprocess

# CSV file path
CSV_FILE_PATH = os.path.expanduser("~/tiktok_download_queue.csv")
DEFAULT_SAVE_PATH = os.path.expanduser(r"C:\Users\wilco\Videos\to edit\TikTok Songs")


def read_queue():
    """Read queued links and their statuses."""
    queue = []
    if os.path.exists(CSV_FILE_PATH):
        with open(CSV_FILE_PATH, mode="r", encoding="utf-8") as csvfile:
            reader = csv.reader(csvfile)
            queue = [(row[0], row[1]) for row in reader if len(row) == 2]
    return queue


def update_queue(queue):
    """Update the queue in the CSV file."""
    with open(CSV_FILE_PATH, mode="w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(queue)


def download_audio():
    """Download audio for pending links and update their status."""
    queue = read_queue()
    updated_queue = []

    os.makedirs(DEFAULT_SAVE_PATH, exist_ok=True)

    for link, status in queue:
        if status == "Pending":
            try:
                subprocess.run([
                    "yt-dlp",
                    "-x", "--audio-format", "mp3",
                    "-o", f"{DEFAULT_SAVE_PATH}/%(title)s.%(ext)s",
                    link
                ], check=True)
                print(f"Downloaded: {link}")
                updated_queue.append((link, "Downloaded"))
            except subprocess.CalledProcessError as e:
                print(f"Error downloading {link}: {e}")
                updated_queue.append((link, "Error"))
        else:
            updated_queue.append((link, status))

    update_queue(updated_queue)
    print("Queue processing complete.")


if __name__ == "__main__":
    download_audio()
