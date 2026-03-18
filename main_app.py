from rich.console import Console

import persistence
import display_utils
import achievements_sharing
import sessions

console = Console()
session_history = []

def main():
    persistence.load_leaderboard()

    user_name = console.input("Enter your name: ")

    while True:
        console.print("\n1. Focus\n2. Pomodoro\n3. Analytics\n4. Exit")

        choice = console.input("Choice: ")

        if choice == "1":
            data = sessions.run_focus_session(user_name)
        elif choice == "2":
            data = sessions.run_pomodoro_session(user_name)
        elif choice == "3":
            display_utils.display_analytics(user_name, session_history, persistence.leaderboard)
            display_utils.display_leaderboard(user_name, persistence.leaderboard)

            continue
        elif choice == "4":
            break
        else:
            continue

        if data:
            session_history.append(data)
            achievements_sharing.check_achievements(data, user_name)

    display_utils.display_leaderboard(user_name, persistence.leaderboard)


if __name__ == "__main__":
    main()