from chat import retrieve, ask

tests = [
    ("What is the refund period?", "30 days"),
    ("Who is the manager of the team?", "Ravi"),
    ("Where is the office located?", "Bengaluru"),
    ("What are the support timings?", "9 AM"),
]

# Eval 1: did retrieval find the right chunk? (no LLM needed)
hits = 0
for question, expected in tests:
    chunks = retrieve(question)
    if any(expected.lower() in c["text"].lower() for c in chunks):
        hits += 1
print(f"Retrieval score: {hits}/{len(tests)}")

# Eval 2: is the final answer correct?
correct = 0
for question, expected in tests:
    answer = ask(question)
    ok = expected.lower() in answer.lower()
    correct += ok
    print(("PASS" if ok else "FAIL"), "-", question)
print(f"Answer score: {correct}/{len(tests)}")