import random
from flask import url_for


# --- Game Logic for Addition Game ---

MAX_VALUE = 20
NUM_OPTIONS = 4

def generate_question():
    op = random.choice(["+", "-"])

    if op == "+":
        a = random.randint(0, MAX_VALUE)
        b = random.randint(0, MAX_VALUE - a)
        correct = a + b
        text = f"{a} + {b} = ?"
    else:
        a = random.randint(0, MAX_VALUE)
        b = random.randint(0, a)
        correct = a - b
        text = f"{a} - {b} = ?"

    options = {correct}
    while len(options) < NUM_OPTIONS:
        candidate = correct + random.choice([-3, -2, -1, 1, 2, 3, -4, 4])
        if 0 <= candidate <= MAX_VALUE:
            options.add(candidate)
        else:
            options.add(random.randint(0, MAX_VALUE))

    options = list(options)
    random.shuffle(options)

    return {
        "text": text,
        "correct": correct,
        "options": options
    }


# --- Game Logic for Multiplication Game (2x table) ---

def make_choices(correct: int):
    wrongs = set()

    while len(wrongs) < 3:
        delta = random.choice([-6, -4, -2, 2, 4, 6, 8, -8])
        w = correct + delta

        if w <= 0 or w == correct:
            continue

        wrongs.add(w)

    choices = [correct] + list(wrongs)
    random.shuffle(choices)
    return choices



# Formatting logic for displaying score and progress

def format_elapsed_ms(elapsed_ms):
    try:
        total_ms = max(0, int(elapsed_ms))
    except (TypeError, ValueError):
        total_ms = 0

    total_seconds = total_ms // 1000
    minutes, seconds = divmod(total_seconds, 60)

    if minutes:
        return f"{minutes} dakika {seconds} saniye"
    return f"{seconds} saniye"
