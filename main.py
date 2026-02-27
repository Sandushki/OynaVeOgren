from flask import Flask, jsonify, request, render_template, session, url_for, redirect

import json
import random
import os

from game_logic import *
from vocabulary import matching_pairs, memory_pairs

app = Flask(__name__)

# 🔐 Required for session support
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "top-secret-key")


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
# Addition + Subtraction Game
# ---------------------------

@app.route("/addition", methods=["GET", "POST"])
def addition():
    # First time entering page → initialize game
    if "question" not in session:
        session["score"] = 0
        session["question_number"] = 0
        session["last_feedback"] = None
        session["question"] = generate_question()

    if request.method == "POST":
        chosen = request.form.get("answer")
        correct = session["question"]["correct"]

        if chosen is not None:
            chosen = int(chosen)
            session["question_number"] += 1

            if chosen == correct:
                session["score"] += 1
                session["last_feedback"] = "✅ Doğru!"
            else:
                session["last_feedback"] = f"❌ Yanlış. Doğru cevap: {correct}"

            session["question"] = generate_question()

        return redirect(url_for("addition"))

    return render_template(
        "addition.html",
        question=session["question"],
        score=session["score"],
        question_number=session["question_number"],
        last_feedback=session["last_feedback"],
    )


@app.route("/reset", methods=["POST"])
def reset():
    session.clear()
    return redirect(url_for("addition"))


# ---------------------------
# Multiplication Game (2x table)
# ---------------------------

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
    return render_template("match.html",
                           pairs=matching_pairs,
                           title="İngilizce Kelime Eşleştirme Oyunu")


@app.post("/submit-match")
def submit_match():
    payload = json.loads(request.form.get("results_json", "{}"))
    return payload


# ---------------------------
# Memory Game
# ---------------------------

@app.get("/memory")
def memory():

    return render_template(
        "memory.html",
        title="Hafıza Kartları Oyunu",
        pairs=memory_pairs
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