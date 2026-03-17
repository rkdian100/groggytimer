import random

MOTIVATIONAL_QUOTES = {
    0: {  # No distractions
        "Goggins": "Amazing, {user_name}! You’re laser-focused like David Goggins powering through a challenge! 💪",
        "Peterson": "Impressive, {user_name}! Your focus reflects order amidst chaos—just like Jordan Peterson says! 🌟",
        "Cobain": "Excellent, {user_name}! No distractions here—raw determination like Kurt Cobain’s passion! 🎸",
        "Ellen": "Fantastic, {user_name}! You’re shining brightly, keeping it positive like Ellen DeGeneres! ✨",
        "Snoop": "Well done, {user_name}! You’re cruising smoothly, laid-back like Snoop Dogg on a chill track! 🎤"
    },
    1: {  # 1-2 distractions
        "Goggins": "Nice effort, {user_name}! A couple distractions won’t stop you—push on, as Goggins would say! ⚡",
        "Peterson": "Good try, {user_name}! Stay disciplined—chaos is normal, but focus is key! 🧠",
        "Cobain": "No worries, {user_name}! Distractions happen—stay raw and real, like Cobain! 🎧"
    },
    2: {  # 3-5 distractions
        "Goggins": "Stay strong, {user_name}! Distractions are piling—channel Goggins and push through the pain! 🏋️",
        "Peterson": "Focus, {user_name}! The shadow of chaos grows—rein it in with wisdom! ⚖️",
        "Ellen": "Keep going, {user_name}! Focus slipping—let’s find the fun again, Ellen-style! 😅"
    },
    3: {  # 6+ distractions
        "Goggins": "No excuses, {user_name}! Buried in distractions? Rise up like Goggins would! 🔥",
        "Peterson": "Refocus, {user_name}! Chaos reigns—find meaning and order! 🌪️",
        "Cobain": "Push through, {user_name}! Distractions won—grunge it out, Cobain-style! 🎸"
    }
}


def get_quote(distraction_count, user_name, level=0):
    """
    Returns a motivational quote based on the distraction count.
    Level is determined by:
       - 0 distractions: level 0
       - 1-2 distractions: level 1
       - 3-5 distractions: level 2
       - 6+ distractions: level 3
    """
    if distraction_count == 0:
        level = 0
    elif distraction_count <= 2:
        level = 1
    elif distraction_count <= 5:
        level = 2
    else:
        level = 3
    voices = MOTIVATIONAL_QUOTES.get(level, {})
    if voices:
        return random.choice(list(voices.values())).format(user_name=user_name)
    else:
        return f"Keep pushing, {user_name}!"