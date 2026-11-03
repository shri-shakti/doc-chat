\# doc-chat



A small "chat with your documents" tool (RAG) that runs fully on your own computer. No API key and no cost.



\## How it works



1\. Reads the `.txt` and `.md` files in `docs/` and cuts them into chunks.

2\. Turns each chunk into numbers (embeddings) with `sentence-transformers`.

3\. For a question, finds the most similar chunks with numpy.

4\. If no chunk is similar enough, answers "I don't know." without calling the model.

5\. Otherwise sends the chunks and the question to a local model (llama3.2:3b via Ollama).

6\. Prints the answer and the source files (added by the code, not the model).



\## Setup



1\. Install \[Ollama](https://ollama.com) and run `ollama pull llama3.2:3b`.

2\. Create and activate a virtual environment, then install the requirements:



```

python -m venv venv

venv\\Scripts\\Activate.ps1

pip install -r requirements.txt

```



3\. Put your `.txt` or `.md` files in `docs/`.



\## Run



```

python chat.py     # ask questions

python eval.py     # run the test questions

```



\## Evaluation



`eval.py` asks 14 questions: 10 answerable from the docs and 4 that are not in the docs (the correct answer is "I don't know").



| Change | Retrieval | Answer |

|---|---|---|

| Baseline (chunk size 800, min\_score 0.1) | 10/10 | 14/14 |

| Chunk size 200 | 10/10 | 13/14 |

| min\_score 0.5 | 4/10 | 8/14 |



What I learned:

\- A threshold set too high makes the app refuse real questions.

\- Smaller chunks lose context, and a small model can return an empty answer.

\- Changing one setting at a time and re-running the eval shows what actually helps.

\- The eval is small, so these results show the pipeline works, not that it will handle large documents.



\## Next steps



Conversation memory, tool use, and a Rust version of the chunking step.

