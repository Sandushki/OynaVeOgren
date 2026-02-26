import random


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


# --- Pairs List for Matching Game ---
pairs = [
    {"id": 1, "left": "kedi", "right": "cat"},
    {"id": 2, "left": "köpek", "right": "dog"},
    {"id": 3, "left": "kuş", "right": "bird"},
    {"id": 4, "left": "balık", "right": "fish"},
    {"id": 5, "left": "inek", "right": "cow"},
    {"id": 6, "left": "at", "right": "horse"},
    {"id": 7, "left": "tavuk", "right": "chicken"},
    {"id": 8, "left": "ördek", "right": "duck"},
    {"id": 9, "left": "elma", "right": "apple"},
    {"id": 10, "left": "muz", "right": "banana"},
    {"id": 11, "left": "portakal", "right": "orange"},
    {"id": 12, "left": "ekmek", "right": "bread"},
    {"id": 13, "left": "su", "right": "water"},
    {"id": 14, "left": "süt", "right": "milk"},
    {"id": 15, "left": "araba", "right": "car"},
    {"id": 16, "left": "otobüs", "right": "bus"},
    {"id": 17, "left": "tren", "right": "train"},
    {"id": 18, "left": "uçak", "right": "plane"},
    {"id": 19, "left": "ev", "right": "house"},
    {"id": 20, "left": "okul", "right": "school"},
    {"id": 21, "left": "masa", "right": "table"},
    {"id": 22, "left": "sandalye", "right": "chair"},
    {"id": 23, "left": "kitap", "right": "book"},
    {"id": 24, "left": "kalem", "right": "pencil"},
    {"id": 25, "left": "top", "right": "ball"},
    {"id": 26, "left": "güneş", "right": "sun"},
    {"id": 27, "left": "ay", "right": "moon"},
    {"id": 28, "left": "ağaç", "right": "tree"},
    {"id": 29, "left": "çiçek", "right": "flower"},
    {"id": 30, "left": "deniz", "right": "sea"},
]