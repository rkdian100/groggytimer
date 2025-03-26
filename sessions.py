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

from . import utils  # Assuming these files are in the same directory, using relative import
from . import quotes
from . import persistence # For leaderboard access (though ideally, sessions might not directly modify leaderboard)
from . import display_utils # For leaderboard display - consider if this dependency is needed

console = Console()

def run_focus_session(user_name):
    """Runs an advanced focus session with milestones and distraction logging."""
    display_utils.display_leaderboard(user_name, persistence.leaderboard) # Passing leaderboard explicitly
    distraction_count = 0
    task_name = console.input(
        f"[bold green]Hi {user_name}, what task would you like to focus on today? (e.g., Coding, Studying): [/]")

    # Get session duration (HH:MM)
    while True:
        duration_str = console.input(f"Enter session duration for '{task_name}' in HH:MM (e.g., 00:05 for 5 minutes): ")
        total_minutes = utils.parse_time(duration_str)
        if total_minutes is not None and total_minutes > 0:
            break
        console.print("[red]Invalid format or zero duration. Please use HH:MM (e.g., 00:05).[/]")
    total_seconds = total_minutes * 60

    # Prepare milestone quotes lists
    quotes_25 = [q.format(user_name=user_name) for q in quotes.MOTIVATIONAL_QUOTES[0].values()]
    quotes_50 = [q.format(user_name=user_name) for q in quotes.MOTIVATIONAL_QUOTES[1].values()]
    quotes_75 = [q.format(user_name=user_name) for q in quotes.MOTIVATIONAL_QUOTES[2].values()]
    quotes_100 = [q.format(user_name=user_name) for q in quotes.MOTIVATIONAL_QUOTES[3].values()]
    milestone_25_shown = False
    milestone_50_shown = False
    milestone_75_shown = False
    milestone_100_shown = False
    milestone_quotes = []

    animations = ["✨ Focusing...", "🚀 Powering...", "🌱 Growing..."]
    progress = Progress(
        "[progress.description]{task.description}",
        BarColumn(bar_width=None, style="red", complete_style="green", finished_style="green"),
        "[progress.percentage]{task.percentage:>3.0f}%",
        TimeRemainingColumn(),
        TimeElapsedColumn(),
    )
    task = progress.add_task(f"[blue]{random.choice(animations)} {task_name}[/]", total=total_seconds)

    # Register hotkey for logging distractions using 'd'
    def log_distraction():
        nonlocal distraction_count
        distraction_count += 1
        console.print("[yellow]Distraction logged![/]")

    hotkey_id = keyboard.add_hotkey('d', log_distraction)

    # Build modular layout
    layout = Layout()
    layout.split_column(
        Layout(name="header", size=5),
        Layout(name="upper", size=8),
        Layout(name="lower")
    )
    header_text = Text.from_markup(
        "[bold magenta]╔══════════════════════════════════╗\n"
        "║  Groggytimer Productivity Booster ║\n"
        "╚══════════════════════════════════╝[/]"
    )
    layout["header"].update(Panel(header_text, border_style="bright_magenta"))
    layout["upper"].update(
        Panel(
            Text(f"⏳ Time Left: {utils.format_seconds(total_seconds)}\nLet's achieve greatness, {user_name}!",
                 style="bold blue", justify="center"),
            border_style="cyan",
            padding=(1, 1)
        )
    )
    layout["lower"].update(
        Panel(progress, title="Session Progress", border_style="green", subtitle="Stay Focused!", padding=(1, 1))
    )

    start_time = time.time()
    animation_idx = 0

    with Live(layout, refresh_per_second=4):
        while not progress.finished:
            elapsed = time.time() - start_time
            remaining = max(total_seconds - elapsed, 0)
            progress_percent = (elapsed / total_seconds) * 100
            progress.update(task, completed=elapsed)
            if int(elapsed) % 2 == 0:
                animation_idx = (animation_idx + 1) % len(animations)
                progress.update(task, description=f"[blue]{animations[animation_idx]} {task_name}[/]")
            if progress_percent >= 25 and not milestone_25_shown:
                utils.play_beep(500, 200)
                milestone_quotes.append(random.choice(quotes_25))
                milestone_25_shown = True
            if progress_percent >= 50 and not milestone_50_shown:
                utils.play_beep(700, 200)
                milestone_quotes.append(random.choice(quotes_50))
                milestone_50_shown = True
            if progress_percent >= 75 and not milestone_75_shown:
                utils.play_beep(900, 200)
                milestone_quotes.append(random.choice(quotes_75))
                milestone_75_shown = True
            if progress_percent >= 100 and not milestone_100_shown:
                utils.play_beep(1200, 300)
                milestone_quotes.append(random.choice(quotes_100))
                milestone_100_shown = True

            header_update = Text(f"⏳ Time Left: {utils.format_seconds(int(remaining))} ⏳", style="bold blue",
                                    justify="center")
            if milestone_quotes:
                header_update.append("\n" + "\n".join(milestone_quotes[:2]), style="blue")
            layout["upper"].update(Panel(header_update, border_style="cyan", padding=(1, 1)))
            if keyboard.is_pressed('q'):
                console.print(f"[red]Session aborted, {user_name}.[/]")
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
    persistence.leaderboard.append(session_entry) # Accessing and modifying leaderboard
    persistence.save_leaderboard() # Saving leaderboard
    console.print(f"[bold green]Great job, {user_name}! You’ve completed your '{task_name}' session! 🎉[/]")
    quote = quotes.get_quote(distraction_count, user_name)
    console.print(f"[yellow]Distractions: {distraction_count} – {quote}[/]")
    console.print(f"[bold white]Focus Score: {focus_score} – Excellent work, {user_name}![/]")
    share_text = (f"I just completed a productive '{task_name}' session with Groggytimer! "
                  f"My focus score was {focus_score}. #GroggyChallenge #ProductivityBoost "
                  "Try it out and boost your productivity!")
    console.print(f"[bright_cyan]Share your success:\n{share_text}[/]")
    console.input("[bright_cyan]Press Enter to continue...[/]")
    report = f"""
[bold bright_cyan]
┌─────────────────────────────────────────────┐
│ 📊 Productivity Report: {user_name}'s Session │
│ Task: {task_name.ljust(15)}               │
│ Duration: {str(total_minutes).ljust(3)} min              │
│ Distractions: {str(distraction_count).ljust(3)}                │
│ Focus Score: {str(focus_score).ljust(3)}                │
└─────────────────────────────────────────────┘
🔄 Ready to Boost Again? Groggytimer’s Got You!
[/]
"""
    console.print(report)
    persistence.log_session_summary(session_entry, user_name) # Logging session summary
    # check_achievements(session_entry, user_name) # Moved to main_app to control flow better
    return session_entry


def run_pomodoro_session(user_name):
    """Runs a Pomodoro session with work and break phases. The break phase is cancellable."""
    preset_choice = console.input(f"[bold green]{user_name}, choose Pomodoro type: 1. Classic (25/5) 2. Custom: ")
    if preset_choice == '2':
        try:
            work_duration = int(console.input("Enter work duration (minutes): "))
            break_duration = int(console.input("Enter break duration (minutes): "))
        except ValueError:
            console.print("[red]Invalid input. Using classic preset.[/]")
            work_duration, break_duration = 25, 5
    else:
        work_duration, break_duration = 25, 5

    distraction_log = []

    def log_distraction():
        distraction_log.append(datetime.now().strftime("%H:%M:%S"))
        console.print("[yellow]Distraction logged![/]")

    hotkey_id = keyboard.add_hotkey('d', log_distraction)

    # Work Session
    console.print(f"[bold green]Work session started for {work_duration} minutes! Press 'q' to skip.[/]")
    try:
        pygame.mixer.init()
    except Exception:
        pass
    work_start = time.time()
    while time.time() - work_start < work_duration * 60:
        if keyboard.is_pressed('q'):
            console.print("[red]Work session aborted.[/]")
            break
        time.sleep(0.1)
    keyboard.remove_hotkey(hotkey_id)

    # Break Session with cancellation (live progress loop)
    break_total = break_duration * 60
    progress_break = Progress(
        "[progress.description]{task.description}",
        BarColumn(bar_width=None, style="magenta", complete_style="bright_green", finished_style="bright_green"),
        "[progress.percentage]{task.percentage:>3.0f}%",
        TimeRemainingColumn(),
        TimeElapsedColumn()
    )
    break_task = progress_break.add_task(f"[bold magenta]Break Time - Relax![/]", total=break_total)
    layout_break = Layout()
    layout_break.split_column(
        Layout(Panel(Text("Break Session\nPress 'q' to cancel", style="bold cyan"), border_style="bright_blue"),
               name="break_header", size=5),
        Layout(Panel(progress_break, title="Break Progress", border_style="bright_green", padding=(1, 1)),
               name="break_progress")
    )
    break_aborted = False
    with Live(layout_break, refresh_per_second=4):
        break_start = time.time()
        while not progress_break.finished:
            elapsed_break = time.time() - break_start
            progress_break.update(break_task, completed=elapsed_break)
            if keyboard.is_pressed('q'):
                console.print("[red]Break session aborted.[/]")
                break_aborted = True
                break
            time.sleep(0.1)
    if break_aborted:
        console.print("[red]Pomodoro session aborted during break.[/]")
    else:
        console.print("[bold green]Pomodoro cycle complete![/]")
    focus_score = utils.calculate_focus_score(work_duration, len(distraction_log))
    session_entry = {
        "task": "Pomodoro Session",
        "duration": work_duration,
        "distractions": len(distraction_log),
        "score": focus_score,
        "timestamp": datetime.now().isoformat()
    }
    persistence.leaderboard.append(session_entry) # Accessing and modifying leaderboard
    persistence.save_leaderboard() # Saving leaderboard
    console.print(f"[bold green]Pomodoro complete, {user_name}! Focus Score: {focus_score}[/]")
    persistence.log_session_summary(session_entry, user_name) # Logging session summary
    # check_achievements(session_entry, user_name) # Moved to main_app
    return session_entry