import platform
import winsound  # Only works on Windows

def parse_time(time_str):
    """Converts a time string in HH:MM format to total minutes."""
    try:
        hours, minutes = map(int, time_str.split(':'))
        if not (0 <= hours <= 23 and 0 <= minutes <= 59):
            raise ValueError("Invalid time format—please use HH:MM.")
        return hours * 60 + minutes
    except ValueError:
        return None


def format_seconds(seconds):
    """Formats seconds into HH:MM:SS."""
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    secs = seconds % 60
    return f"{int(hours):02d}:{int(minutes):02d}:{int(secs):02d}"


def calculate_focus_score(duration_minutes, distractions):
    """Calculates focus score: duration minus 2 points per distraction."""
    return max(0, duration_minutes - (distractions * 2))


def play_beep(frequency, duration):
    """Plays a beep sound on Windows; silent on other OS."""
    if platform.system() == "Windows":
        try:
            winsound.Beep(frequency, duration)
        except Exception:
            pass