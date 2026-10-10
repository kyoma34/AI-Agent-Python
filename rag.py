from pathlib import Path

from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from ollama import chat


# ==========================================
# 1. Load embedding model
# ==========================================

embedding_model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)


# ==========================================
# 2. Read documents
# ==========================================

DOCUMENTS_DIR = Path("documents")


def load_documents():

    documents = []

    for file_path in DOCUMENTS_DIR.iterdir():

        if file_path.suffix.lower() in [".txt", ".md"]:

            text = file_path.read_text(
                encoding="utf-8"
            )

            documents.append({
                "filename": file_path.name,
                "text": text
            })

    return documents


# ==========================================
# 3. Split text into chunks
# ==========================================

def chunk_text(text, chunk_size=500, overlap=100):

    chunks = []

    start = 0

    while start < len(text):

        end = start + chunk_size

        chunk = text[start:end]

        chunks.append(chunk)

        start += chunk_size - overlap

    return chunks


# ==========================================
# 4. Build knowledge base
# ==========================================

documents = load_documents()

chunks = []

for document in documents:

    document_chunks = chunk_text(
        document["text"]
    )

    for chunk in document_chunks:

        chunks.append({
            "text": chunk,
            "source": document["filename"]
        })


print(f"Loaded {len(documents)} document(s).")
print(f"Created {len(chunks)} chunk(s).")


# ==========================================
# 5. Create embeddings
# ==========================================

chunk_texts = [
    chunk["text"]
    for chunk in chunks
]

chunk_embeddings = embedding_model.encode(
    chunk_texts
)


# ==========================================
# 6. Search knowledge base
# ==========================================

def search_knowledge(query, top_k=3):

    query_embedding = embedding_model.encode(
        [query]
    )

    similarities = cosine_similarity(
        query_embedding,
        chunk_embeddings
    )[0]

    results = sorted(
        zip(chunks, similarities),
        key=lambda x: x[1],
        reverse=True
    )

    return results[:top_k]


# ==========================================
# 7. Ask Qwen
# ==========================================

def ask_qwen(question):

    results = search_knowledge(question)

    context_parts = []

    for chunk, score in results:

        context_parts.append(
            f"Source: {chunk['source']}\n"
            f"{chunk['text']}"
        )

    context = "\n\n".join(
        context_parts
    )

    print("\n--- RETRIEVED CONTEXT ---")
    print(context)
    print("-------------------------")

    prompt = f"""
Answer the user's question using ONLY the
information provided in the context.

If the answer cannot be found in the context,
say that you don't know.

Context:

{context}

User question:

{question}
"""

    response = chat(
        model="qwen3-local",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response.message.content


# ==========================================
# 8. Chat loop
# ==========================================

while True:

    question = input("\nQuestion: ")

    if question.strip().lower() == "exit":
        break

    answer = ask_qwen(question)

    print("\nAnswer:")
    print(answer)