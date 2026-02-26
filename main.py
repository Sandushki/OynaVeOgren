from flask import Flask, jsonify, request, render_template, session, url_for, redirect
import json
import random
import os

app = Flask(__name__)

# 🔐 Required for session support
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "dev-only-change-this")


# ---------------------------
# Static Pages
# ---------------------------

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/games')
def games():
    return render_template('games.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')


# ---------------------------
# Multiplication Game (2x table)
# ---------------------------

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


@app.route("/multiply", methods=["GET", "POST"])
def multiply():

    # Initialize session
    if "b" not in session:
        session["b"] = 1
        session["score"] = 0
        session["progress"] = 1

    message = None
    is_correct = None

    if request.method == "POST":
        selected = int(request.form["answer"])
        correct = 2 * session["b"]

        if selected == correct:
            session["score"] += 1
            message = "Doğru! 🎉"
            is_correct = True
        else:
            message = f"Olmadı 😄 Doğru cevap: {correct}"
            is_correct = False

        session["b"] += 1
        session["progress"] += 1

        # Game finished (2x1 to 2x15)
        if session["b"] > 15:
            final_score = session["score"]
            session.clear()
            return render_template(
                "multiply.html",
                question={"a": 2, "b": 1},
                choices=[2, 4, 6, 8],
                score=final_score,
                progress=15,
                message=f"Oyun bitti! Toplam puan: {final_score}/15 🎉",
                is_correct=True
            )

    b = session["b"]
    question = {"a": 2, "b": b}
    choices = make_choices(2 * b)

    return render_template(
        "multiply.html",
        question=question,
        choices=choices,
        score=session["score"],
        progress=session["progress"],
        message=message,
        is_correct=is_correct
    )


# ---------------------------
# Match Game
# ---------------------------

@app.get("/match")
def match():
    pairs = [
        {"id": 1, "left": "kedi", "right": "cat"},
        {"id": 2, "left": "köpek", "right": "dog"},
        {"id": 3, "left": "kuş", "right": "bird"},
    ]
    return render_template("match.html", pairs=pairs, title="İngilizce Kelime Eşleştirme Oyunu")


@app.post("/submit-match")
def submit_match():
    payload = json.loads(request.form.get("results_json", "{}"))
    return payload


# ---------------------------
# Memory Game
# ---------------------------

@app.get("/memory")
def memory():

    pairs = [
        {
            "id": 1,
            "word": "kuş",
            "image_url": url_for("static", filename="img/bird.png"),
            "alt": "kuş"
        },
        {
            "id": 2,
            "word": "kedi",
            "image_url": url_for("static", filename="img/cat.png"),
            "alt": "kedi"
        },
        {
            "id": 3,
            "word": "köpek",
            "image_url": url_for("static", filename="img/dog.png"),
            "alt": "köpek"
        },
    ]

    return render_template(
        "memory.html",
        title="Hafıza Kartları Oyunu",
        pairs=pairs
    )


@app.post("/submit-memory")
def submit_memory():
    raw = request.form.get("results_json", "{}")
    results = json.loads(raw)
    print("MEMORY GAME RESULTS:", results)
    return jsonify(results)


# ---------------------------

if __name__ == '__main__':
    app.run(debug=True)