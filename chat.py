import os, glob
import numpy as np
import ollama
from sentence_transformers import SentenceTransformer

embedder = SentenceTransformer("all-MiniLM-L6-v2")

def load_chunks(folder, size=800, overlap=100):
    chunks = []
    for path in glob.glob(f"{folder}/*.txt") + glob.glob(f"{folder}/*.md"):
        text = open(path, encoding="utf-8").read()
        for i in range(0, len(text), size - overlap):
            chunks.append({"source": os.path.basename(path),
                           "text": text[i:i + size]})
    return chunks

chunks = load_chunks("docs")
vectors = embedder.encode([c["text"] for c in chunks],
                          normalize_embeddings=True)

def retrieve(question, k=2, min_score=0.1):
    q = embedder.encode([question], normalize_embeddings=True)[0]
    scores = vectors @ q
    top = np.argsort(scores)[::-1][:k]
    return [chunks[i] for i in top if scores[i] >= min_score]

def ask(question):
    top = retrieve(question)
    if not top:
        return "I don't know."
    context = "\n\n".join(c["text"] for c in top)
    response = ollama.chat(
        model="llama3.2:3b",
        messages=[
            {"role": "system",
             "content": ("Answer using only the context. Give a short answer. "
                         "If the answer is not written in the context, "
                         "reply exactly: I don't know.")},
            {"role": "user",
             "content": f"Context:\n{context}\n\nQuestion: {question}"},
        ],
        options={"temperature": 0},
    )
    sources = sorted({c["source"] for c in top})
    return response["message"]["content"] + f"\n(Sources: {', '.join(sources)})"

if __name__ == "__main__":
    while True:
        q = input("\nAsk (or 'quit'): ")
        if q == "quit":
            break
        print(ask(q))