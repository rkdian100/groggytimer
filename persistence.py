import os
import json
from rich.console import Console
from datetime import datetime

LEADERBOARD_FILE = "leaderboard.json"
SESSION_LOG_FILE = "session_log.txt"

console = Console()
leaderboard = []  # Persistent leaderboard will be loaded here


def load_leaderboard():
    global leaderboard
    if os.path.exists(LEADERBOARD_FILE):
        try:
            with open(LEADERBOARD_FILE, "r") as f:
                leaderboard = json.load(f)
        except Exception as e:
            console.print(f"[red]Error loading leaderboard: {e}[/]")
            leaderboard = []
    else:
        leaderboard = []


def save_leaderboard():
    try:
        with open(LEADERBOARD_FILE, "w") as f:
            json.dump(leaderboard, f, indent=4)
    except Exception as e:
        console.print(f"[red]Error saving leaderboard: {e}[/]")


def log_session_summary(session_data, user_name):
    """Appends a session summary to the log file."""
    summary_line = (
        f"{datetime.now().isoformat()} | {user_name} | {session_data['task']} | "
        f"Duration: {session_data['duration']} min | "
        f"Distractions: {session_data['distractions']} | "
        f"Focus Score: {session_data['score']}\n"
    )
    try:
        with open(SESSION_LOG_FILE, "a") as f:
            f.write(summary_line)
    except Exception as e:
        console.print(f"[red]Error writing to log file: {e}[/]")