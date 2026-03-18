import time
import random
import keyboard
import pygame
from datetime import datetime
from rich.console import Console
from rich.progress import Progress, BarColumn, TimeRemainingColumn, TimeElapsedColumn
from rich.live import Live
from rich.panel import Panel
from rich.text import Text
from rich.layout import Layout

import utils
import quotes
import persistence
import display_utils


console = Console()

def run_focus_session(user_name):
    display_utils.display_leaderboard(user_name, persistence.leaderboard)

    distraction_count = 0
    task_name = console.input(
        f"[bold green]Hi {user_name}, what task would you like to focus on today? [/]"
    )

    while True:
        duration_str = console.input("Enter session duration (HH:MM): ")
        total_minutes = utils.parse_time(duration_str)
        if total_minutes and total_minutes > 0:
            break
        console.print("[red]Invalid format. Try again.[/]")

    total_seconds = total_minutes * 60

    progress = Progress(
        "[progress.description]{task.description}",
        BarColumn(),
        "[progress.percentage]{task.percentage:>3.0f}%",
        TimeRemainingColumn(),
        TimeElapsedColumn(),
    )

    task = progress.add_task(f"[blue]{task_name}[/]", total=total_seconds)

    def log_distraction():
        nonlocal distraction_count
        distraction_count += 1
        console.print("[yellow]Distraction logged![/]")

    hotkey_id = keyboard.add_hotkey('9', log_distraction)

    start_time = time.time()

    with Live(progress, refresh_per_second=4):
        while not progress.finished:
            elapsed = time.time() - start_time
            progress.update(task, completed=elapsed)

            if keyboard.is_pressed('q'):
                console.print("[red]Session aborted[/]")
                keyboard.remove_hotkey(hotkey_id)
                return None

            time.sleep(0.1)

    keyboard.remove_hotkey(hotkey_id)

    focus_score = utils.calculate_focus_score(total_minutes, distraction_count)

    session_entry = {
        "task": task_name,
        "duration": total_minutes,
        "distractions": distraction_count,
        "score": focus_score,
        "timestamp": datetime.now().isoformat()
    }

    persistence.leaderboard.append(session_entry)
    persistence.save_leaderboard()
    persistence.log_session_summary(session_entry, user_name)

    console.print(f"[green]Done! Score: {focus_score}[/]")

    return session_entry


def run_pomodoro_session(user_name):
    work_duration = 25
    break_duration = 5

    console.print("[green]Pomodoro started[/]")

    time.sleep(work_duration * 60)

    console.print("[cyan]Break time[/]")
    time.sleep(break_duration * 60)

    focus_score = utils.calculate_focus_score(work_duration, 0)

    session_entry = {
        "task": "Pomodoro",
        "duration": work_duration,
        "distractions": 0,
        "score": focus_score,
        "timestamp": datetime.now().isoformat()
    }

    persistence.leaderboard.append(session_entry)
    persistence.save_leaderboard()

    return session_entry