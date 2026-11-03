from chat import retrieve, ask

# (question, expected text). None means "not in the notes".
tests = [
    ("What is the refund period?", "30 days"),
    ("Who is the manager of the team?", "Ravi"),
    ("Where is the office located?", "Bengaluru"),
    ("What are the support timings?", "9 AM"),
    ("Who is the CEO?", "Shrishakti"),
    ("What is the company's phone number?", None),
    ("At what time do I study Rust every day?", "7 PM"),
    ("What is the name of my practice project?", "logtool"),
    ("Which chapter of the Rust book am I reading?", "chapter 4"),
    ("Who is my Rust mentor?", "Priya"),
    ("Which crate do I use for argument parsing?", "clap"),
    ("Who won the 2018 World Cup?", None),
    ("What is the capital of France?", None),
    ("What is my favorite food?", None),
]

def says_unknown(answer):
    a = answer.lower().replace("’", "'")
    return "don't know" in a or "do not know" in a

hits = 0
answerable = 0
correct = 0

for question, expected in tests:
    answer = ask(question)

    if expected is None:
        ok = says_unknown(answer)
    else:
        answerable += 1
        chunks = retrieve(question)
        if any(expected.lower() in c["text"].lower() for c in chunks):
            hits += 1
        ok = expected.lower() in answer.lower()

    correct += ok
    print("PASS" if ok else "FAIL", "-", question)
    if not ok:
        print("   Got:", answer)

print(f"Retrieval score: {hits}/{answerable}")
print(f"Answer score: {correct}/{len(tests)}")