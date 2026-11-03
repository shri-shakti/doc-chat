import os, glob
import numpy as np
import ollama
from anthropic import Anthropic
from sentence_transformers import SentenceTransformer

client = Anthropic()  # reads ANTHROPIC_API_KEY
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

def retrieve(question, k=4):
    q = embedder.encode([question], normalize_embeddings=True)[0]
    scores = vectors @ q                      # cosine similarity
    top = np.argsort(scores)[::-1][:k]
    return [chunks[i] for i in top]

def ask(question):
    context = "\n\n".join(
        f"[{c['source']}]\n{c['text']}" for c in retrieve(question))
    response = ollama.chat(
        model="llama3.2:3b",
        messages=[
            {"role": "system",
             "content": ("Answer using only the provided context. "
                         "If the answer isn't there, say you don't know. "
                         "Mention the source file names you used.")},
            {"role": "user",
             "content": f"Context:\n{context}\n\nQuestion: {question}"},
        ],
    )
    return response["message"]["content"]

# while True:
#     q = input("\nAsk (or 'quit'): ")
#     if q == "quit":
#         break
#     print(ask(q))

if __name__ == "__main__":
    while True:
        q = input("\nAsk (or 'quit'): ")
        if q == "quit":
            break
        print(ask(q))