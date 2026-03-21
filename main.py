from flask import Flask, request, render_template, session, url_for, redirect

import json
import random
import os
import time

from game_logic import *
from vocabulary import matching_pairs, memory_pairs

app = Flask(__name__)

# 🔐 Required for session support
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "top-secret-key")

ADDITION_DURATION_SECONDS = 120



# ---------------------------
# Helper Functions
# ---------------------------

def parse_results_payload():
    raw = request.form.get("results_json", "{}")

    try:
        return json.loads(raw)
    except (TypeError, json.JSONDecodeError):
        return {}


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


def render_addition_results():
    correct = int(session.get("score", 0) or 0)
    wrong = int(session.get("wrong_answers", 0) or 0)
    total = correct + wrong

    session.clear()

    return render_template(
        "game_results.html",
        title="Toplama ve Çıkarma Sonuçları",
        heading="Süre Doldu!",
        subtitle="2 dakikalık oyun tamamlandı. Hadi sonuçlarına bakalım.",
        stats=[
            {"label": "Doğru Sayısı", "value": correct},
            {"label": "Yanlış Sayısı", "value": wrong},
            {"label": "Toplam Soru", "value": total},
        ],
        primary_action={"label": "Yeniden Oyna", "url": url_for("addition")},
        secondary_action={"label": "Ana Sayfaya Dön", "url": url_for("index")},
    )



# -----------------------------
# Static Pages
# -----------------------------

@app.route('/')
def index():
    return render_template('index.html')


# -----------------------------
# Addition + Subtraction Game
# -----------------------------

@app.route("/addition", methods=["GET", "POST"])
def addition():
    # First time entering page → initialize game
    if "question" not in session:
        session["score"] = 0
        session["wrong_answers"] = 0
        session["question_number"] = 0
        session["last_feedback"] = None
        session["question"] = generate_question()
        session["addition_started_at"] = int(time.time())

    if "score" not in session:
        session["score"] = 0
    if "wrong_answers" not in session:
        session["wrong_answers"] = 0
    if "question_number" not in session:
        session["question_number"] = 0
    if "last_feedback" not in session:
        session["last_feedback"] = None
    if "addition_started_at" not in session:
        session["addition_started_at"] = int(time.time())

    started_at = int(session.get("addition_started_at", int(time.time())))
    elapsed_seconds = max(0, int(time.time()) - started_at)
    remaining_seconds = max(0, ADDITION_DURATION_SECONDS - elapsed_seconds)

    if request.method == "POST" and request.form.get("action") == "finish":
        return render_addition_results()

    if remaining_seconds <= 0:
        return render_addition_results()

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
                session["wrong_answers"] += 1
                session["last_feedback"] = f"❌ Yanlış. Doğru cevap: {correct}"

            session["question"] = generate_question()

        return redirect(url_for("addition"))

    return render_template(
        "addition.html",
        question=session["question"],
        score=session["score"],
        wrong_answers=session["wrong_answers"],
        question_number=session["question_number"],
        last_feedback=session["last_feedback"],
        remaining_seconds=remaining_seconds,
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
                           title="Dijital Öğrenme Köprüsü - İngilizce Kelime Eşleştirme Oyunu")


@app.post("/submit-match")
def submit_match():
    payload = parse_results_payload()
    attempts = int(payload.get("attempts", 0) or 0)
    matches = int(payload.get("score", 0) or 0)
    total = int(payload.get("total", 0) or 0)

    return render_template(
        "game_results.html",
        title="İngilizce Kelime Eşleştirme Sonuçları",
        heading="İngilizce Kelime Eşleştirme Oyunu Bitti!",
        subtitle="Harika iş çıkardın! İşte bu turun sonuçları.",
        stats=[
            {"label": "Deneme Sayısı", "value": attempts},
            {"label": "Doğru Eşleşme", "value": matches},
            {"label": "Toplam Eşleşme", "value": total},
        ],
        primary_action={"label": "Yeniden Oyna", "url": url_for("match")},
        secondary_action={"label": "Ana Sayfaya Dön", "url": url_for("index")},
    )


# ---------------------------
# Memory Game
# ---------------------------

@app.get("/memory")
def memory():

    return render_template(
        "memory.html",
        title="Dijital Öğrenme Köprüsü - Hafıza Kartları Oyunu",
        pairs=memory_pairs
    )


@app.post("/submit-memory")
def submit_memory():
    results = parse_results_payload()
    moves = int(results.get("moves", 0) or 0)
    matches = int(results.get("matches", 0) or 0)
    elapsed_ms = int(results.get("elapsed_ms", 0) or 0)

    return render_template(
        "game_results.html",
        title="Hafıza Kartları Sonuçları",
        heading="Hafıza Kartları Oyunu Bitti!",
        subtitle="Süper hafıza! Bu turdaki başarın burada.",
        stats=[
            {"label": "Hamle Sayısı", "value": moves},
            {"label": "Eşleşme Sayısı", "value": matches},
            {"label": "Geçen Süre", "value": format_elapsed_ms(elapsed_ms)},
        ],
        primary_action={"label": "Yeniden Oyna", "url": url_for("memory")},
        secondary_action={"label": "Ana Sayfaya Dön", "url": url_for("index")},
    )


# ---------------------------

if __name__ == '__main__':
    app.run(debug=True)
