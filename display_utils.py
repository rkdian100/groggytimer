from rich.console import Console
from rich.table import Table

console = Console()

def display_leaderboard(user_name, leaderboard):
    """Displays the top 5 sessions from the persistent leaderboard."""
    if not leaderboard:
        console.print(f"[yellow]No sessions yet, {user_name}! Start building your productivity legacy! 📈[/]")
        return
    sorted_board = sorted(leaderboard, key=lambda x: x["score"], reverse=True)
    top_5 = sorted_board[:5]
    console.print(f"[bold blue]=== 🏆 {user_name}'s Productivity Leaderboard with Groggytimer 🏆 ===[/]")
    table = Table(title="", style="bright_magenta", title_style="bold green")
    table.add_column("Rank", justify="center", style="cyan", no_wrap=True)
    table.add_column("Task", justify="left", style="green", no_wrap=True)
    table.add_column("Duration", justify="center", style="yellow", no_wrap=True)
    table.add_column("Distractions", justify="center", style="red", no_wrap=True)
    table.add_column("Focus Score", justify="center", style="bold white", no_wrap=True)
    for i, session in enumerate(top_5, 1):
        row_style = "bold green" if i == 1 else ""
        table.add_row(
            str(i),
            session["task"],
            f"{session['duration']} min",
            str(session["distractions"]),
            str(session["score"]),
            style=row_style
        )
    console.print(table)
    console.print(f"[blue]Keep shining, {user_name}! Groggytimer’s here to help you excel! 🌟[/]\n")


def display_analytics(user_name, session_history):
    """Displays simple analytics from session history."""
    if not session_history:
        console.print(f"[yellow]No session data available for analytics, {user_name}.[/]")
        return
    total_sessions = len(session_history)
    total_duration = sum(s["duration"] for s in session_history)
    avg_score = sum(s["score"] for s in session_history) / total_sessions
    console.print(f"[bold green]Analytics for {user_name}:[/]")
    console.print(f"Total Sessions: {total_sessions}")
    console.print(f"Total Duration: {total_duration} min")
    console.print(f"Average Focus Score: {avg_score:.1f}")