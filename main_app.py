import os

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'  # Suppress pygame welcome message

import time
import random
import keyboard
import pygame
from rich.console import Console

import persistence
import utils
import quotes
import display_utils
import achievements_sharing
import sessions


console = Console()
session_history = []  # In-memory session history


###############################
# MAIN MENU & APPLICATION
###############################
def main():
    persistence.load_leaderboard()
    console.clear()
    console.print(
        "[bold bright_magenta]\n"
        "╔════════════════════════════════════════╗\n"
        "║   Groggytimer Productivity Boost Hub   ║\n"
        "╚════════════════════════════════════════╝\n"
        "[/bold bright_magenta]"
    )
    user_name = console.input("[bold bright_blue]Hello, friend! What's your name? [/]")
    console.print(f"[bold bright_blue]Welcome, {user_name}! Groggytimer is here to maximize your productivity! 🚀[/]")

    while True:
        console.print("[bold cyan]Choose session type:[/]")
        console.print("1. Focus Session (Advanced with Milestones & Motivational Quotes)")
        console.print("2. Pomodoro Session (Enhanced with Break Cancellation)")
        console.print("3. View Analytics & Achievements")
        console.print("4. Join Focus Room (Collaborative Challenge) [Coming Soon]")
        session_type = console.input("Enter 1, 2, 3 or 4: ")
        session_data = None

        if session_type == '1':
            session_data = sessions.run_focus_session(user_name)
            if session_data is None:
                continue  # Aborted session, go back to menu
            session_history.append(session_data)
            achievements_sharing.share_on_social_media(session_data, user_name) # moved share here for main app control
            achievements_sharing.check_achievements(session_data, user_name) # moved achievement check here
        elif session_type == '2':
            session_data = sessions.run_pomodoro_session(user_name)
            session_history.append(session_data)
            achievements_sharing.share_on_social_media(session_data, user_name) # moved share here
            achievements_sharing.check_achievements(session_data, user_name) # moved achievement check here
        elif session_type == '3':
            display_utils.display_analytics(user_name, session_history) # Passing session_history
            console.input("[bright_cyan]Press Enter to return to the menu...[/]")
            continue
        elif session_type == '4':
            achievements_sharing.join_focus_room(user_name)
            console.input("[bright_cyan]Press Enter to return to the menu...[/]")
            continue
        else:
            console.print("[red]Invalid choice. Please choose 1, 2, 3 or 4.[/]")
            continue

        if console.input(
                f"[bright_cyan]Would you like to start another session, {user_name}? (y/n): [/]").lower() != 'y':
            break

    console.print("\n[bold bright_blue]=== Final Productivity Rankings with Groggytimer ===[/]")
    display_utils.display_leaderboard(user_name, persistence.leaderboard) # Passing leaderboard
    console.print(
        f"[bright_blue]Thank you, {user_name}! Stay focused and inspired—share your success with #GroggyChallenge! 🌟[/]")


if __name__ == "__main__":
    main()