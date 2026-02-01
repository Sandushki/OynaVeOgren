from flask import Flask, jsonify, request, render_template, url_for, redirect, json
import json

app = Flask(__name__)


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

@app.get("/match")
def match():
    pairs = [
        {"id": 1, "left": "kedi", "right": "cat"},
        {"id": 2, "left": "köpek", "right": "dog"},
        {"id": 3, "left": "kuş", "right": "bird"},
    ]
    return render_template("match.html", pairs=pairs, title="Kelime Eşleştirme Oyunu")

@app.post("/submit-match")
def submit_match():
    payload = json.loads(request.form.get("results_json", "{}"))
    # TODO: store payload in DB/session, compute grade, etc.
    return payload  # or redirect(url_for("match"))

@app.get("/memory")
def memory():
    """Memory game page"""

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
        title="Kelime – Resim Hafıza Oyunu",
        pairs=pairs
    )


@app.post("/submit-memory")
def submit_memory():
    """
    Receives results from the memory game.
    Payload comes from hidden input 'results_json'.
    """

    raw = request.form.get("results_json", "{}")
    results = json.loads(raw)

    # TODO: store in DB, session, analytics, grading, etc.
    print("MEMORY GAME RESULTS:", results)

    # For now, just return JSON (or redirect)
    return jsonify(results)



if __name__ == '__main__':

    app.run(debug=True)