import oracledb
from mymodel import QAModel
from preprocess import BM25Retriever

# =========================
# GLOBAL EXIT FUNCTION
# =========================
def check_exit(user_input):
    if user_input.lower() == "exit":
        print("Exiting...")
        exit()

# =========================
# CONNECT ORACLE
# =========================
conn = oracledb.connect(
    user="system",      
    password="root",    
    dsn="localhost:1521/XE"
)

cursor = conn.cursor()

print("Connected to Oracle")

# =========================
# FETCH DATA (CLOB FIX)
# =========================
cursor.execute("SELECT content FROM news_articles")

documents = [
    row[0].read() if row[0] else ""
    for row in cursor.fetchall()
]

print("Loaded documents:", len(documents))

# =========================
# INIT SYSTEM
# =========================
retriever = BM25Retriever(documents)
model = QAModel()

# =========================
# MAIN LOOP
# =========================
while True:
    query = input("\nEnter your query (or type 'exit'): ")
    check_exit(query)

    results = retriever.search(query, top_k=10)
    page = 0

    while True:
        # Prevent overflow
        if page * 5 >= len(results):
            print("No more results")
            page -= 1
            continue

        print(f"\nShowing results {page*5 + 1} to {min((page+1)*5, len(results))}:")

        current_results = results[page*5:(page+1)*5]

        for i, doc in enumerate(current_results, start=1):
            print(f"\n[{i}] {doc[:150]}...")

        choice = input("\nSelect article (1-5), 'n' for next, 'b/back': ")
        check_exit(choice)

        # NEXT PAGE
        if choice.lower() == 'n':
            if (page + 1) * 5 < len(results):
                page += 1
            else:
                print("No more results")
            continue

        # BACK TO QUERY
        elif choice.lower() in ['b', 'back']:
            break

        # SELECT ARTICLE
        elif choice in ['1','2','3','4','5']:
            index = page*5 + int(choice) - 1

            if index >= len(results):
                print("Invalid selection")
                continue

            selected_doc = results[index]

            print("\nSelected Article:")
            print(selected_doc[:300])

            # =========================
            # QUESTION LOOP
            # =========================
            while True:
                question = input("\nAsk a question ('back' or 'exit'): ")
                check_exit(question)

                if question.lower() == "back":
                    break

                question_lower = question.lower()

                # =========================
                # SUMMARY HANDLING (FIRST)
                # =========================
                if "about" in question_lower or "summary" in question_lower:
                    print("\nAnswer (summary):")

                    sentences = selected_doc.split(".")
                    summary = ". ".join(sentences[:2])

                    print(summary.strip(), "...")
                    continue

                # =========================
                # VALIDATION
                # =========================
                if len(question.strip()) < 5:
                    print("Please ask a meaningful question.")
                    continue

                valid_words = ["what", "who", "when", "where", "why", "how", "which"]

                if not any(word in question_lower for word in valid_words):
                    print("Please ask a proper question.")
                    continue

                # =========================
                # QA MODEL
                # =========================
                answer = model.get_answer(question, selected_doc)

                if not answer:
                    print("No reliable answer found.")
                else:
                    print("\nAnswer:", answer)

                    # STORE QUERY
                    cursor.execute(
                        "INSERT INTO queries (user_query, question, answer) VALUES (:1, :2, :3)",
                        (query, question, answer)
                    )
                    conn.commit()

        else:
            print("Invalid choice")
