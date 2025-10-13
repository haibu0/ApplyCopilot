import sqlite3
import os



import sqlite3, os, json

n8n_response = {
    "tailored_resume": "This is a placeholder resume text.",
    "resume_stats": {
        "Experience": 70,
        "Skills": 80,
        "Education": 65,
        "Projects": 75,
        "Certifications": 60
    },
    "coverageSummary": "Summary of resume coverage goes here.",
    "cover_letter": "This is a placeholder cover letter.",
    "recruiter_email": {
        "subject": "Application for Placeholder Role",
        "body": "Dear Recruiter, here is a simple placeholder email body."
    },
    "recruiter_message": "Hi, this is a placeholder chat message to recruiter.",
    "metadata": {
        "strategy_notes": "These are placeholder strategy notes.",
        "tone": "Professional, concise, and confident."
    }
}

if os.path.exists("demo.db"):
    os.remove("demo.db")

conn = sqlite3.connect("demo.db")
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS notes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    data TEXT
);
""")

# save dictionary as JSON string
cur.execute("INSERT INTO notes (data) VALUES (?)", (json.dumps(n8n_response),))
conn.commit()

# get it back
cur.execute("SELECT data FROM notes")
row = cur.fetchone()
saved_dict = json.loads(row[0])   # convert JSON back to Python dict


print(saved_dict["tailored_resume"])   # 👉 "This is a placeholder resume text."
print(saved_dict["cover_letter"])      # 👉 "This is a placeholder cover letter."
print(saved_dict["resume_stats"]["Skills"])  # 👉 80
