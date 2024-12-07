from flask import Flask, request, render_template_string
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash
import csv
import os

app = Flask(__name__)
auth = HTTPBasicAuth()

# User credentials (add more users if needed)
users = {
    "scarylasers": generate_password_hash("Binx.67087"),  # Change this to your preferred credentials
}


@auth.verify_password
def verify_password(username, password):
    if username in users and check_password_hash(users.get(username), password):
        return username


# Default CSV file path
CSV_FILE_PATH = os.path.expanduser("~/tiktok_download_queue.csv")

# HTML template
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>TikTok Queue Manager</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; padding: 0; }
        textarea { width: 100%; height: 100px; }
        button { margin-top: 10px; padding: 10px 20px; background-color: #007bff; color: white; border: none; cursor: pointer; }
        button:hover { background-color: #0056b3; }
        .success { color: green; }
        table { width: 100%; border-collapse: collapse; margin-top: 20px; }
        th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
        th { background-color: #f2f2f2; }
    </style>
</head>
<body>
    <h1>TikTok Queue Manager</h1>
    <form method="POST">
        <label for="links">Paste TikTok Links (one per line):</label>
        <textarea name="links" id="links" placeholder="Enter TikTok links here..."></textarea>
        <br>
        <button type="submit">Add to Queue</button>
    </form>
    {% if message %}
        <p class="success">{{ message }}</p>
    {% endif %}
    <h3>Queued Links:</h3>
    <table>
        <tr>
            <th>Link</th>
            <th>Status</th>
        </tr>
        {% for link, status in queued_links %}
            <tr>
                <td>{{ link }}</td>
                <td>{{ status }}</td>
            </tr>
        {% endfor %}
    </table>
</body>
</html>
"""


def read_queue():
    """Read the queue from the CSV file."""
    if os.path.exists(CSV_FILE_PATH):
        with open(CSV_FILE_PATH, mode="r", encoding="utf-8") as csvfile:
            reader = csv.reader(csvfile)
            return [(row[0], row[1]) for row in reader if len(row) == 2]
    return []


def add_links_to_queue(links):
    """Add new links to the CSV queue."""
    with open(CSV_FILE_PATH, mode="a", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        for link in links:
            writer.writerow([link, "Pending"])


@app.route("/test")
def test():
    return "The app is running on Heroku!"


    queued_links = read_queue()
    return render_template_string(HTML_TEMPLATE, message=message, queued_links=queued_links)


import os
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
