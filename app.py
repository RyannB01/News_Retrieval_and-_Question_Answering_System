from flask import Flask, render_template, request
import oracledb
from mymodel import QAModel
from preprocess import BM25Retriever

app = Flask(__name__)

# =========================
# DB CONNECTION
# =========================
conn = oracledb.connect(
    user="system",       # 🔴 CHANGE
    password="root",   # 🔴 CHANGE
    dsn="localhost:1521/XE"
)
cursor = conn.cursor()

# =========================
# LOAD DATA
# =========================
cursor.execute("SELECT content FROM news_articles")

documents = [
    row[0].read() if row[0] else ""
    for row in cursor.fetchall()
]

retriever = BM25Retriever(documents)
model = QAModel()

# 🔥 GLOBAL STORAGE
global_results = []
global_query = ""

# =========================
# HOME
# =========================
@app.route("/", methods=["GET", "POST"])
def index():
    global global_results, global_query

    if request.method == "POST":
        query = request.form["query"]
        global_query = query

        global_results = retriever.search(query, top_k=50)

        return render_template(
            "results.html",
            results=global_results,
            query=query,
            page=0
        )

    return render_template("index.html")


# =========================
# PAGINATION
# =========================
@app.route("/results", methods=["POST"])
def results_page():
    page = int(request.form["page"])

    return render_template(
        "results.html",
        results=global_results,
        query=global_query,
        page=page
    )


# =========================
# ARTICLE + QA
# =========================
@app.route("/article", methods=["POST"])
def article():
    selected_doc = request.form["document"]
    question = request.form.get("question")

    answer = None
    summary = None

    if question:
        q = question.lower()

        # SUMMARY
        if "about" in q or "summary" in q:
            sentences = selected_doc.split(".")
            summary = ". ".join(sentences[:2])

        else:
            answer = model.get_answer(question, selected_doc)

            if not answer:
                answer = "No reliable answer found."

            cursor.execute(
                "INSERT INTO queries (user_query, question, answer) VALUES (:1, :2, :3)",
                ("web", question, answer)
            )
            conn.commit()

    return render_template(
        "article.html",
        document=selected_doc,
        answer=answer,
        summary=summary
    )


if __name__ == "__main__":
    app.run(debug=True)