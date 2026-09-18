import re

from sentence_transformers import SentenceTransformer

from qdrant_client import QdrantClient
from qdrant_client.models import (
    Distance,
    PointStruct,
    VectorParams
)

from langchain_ollama import OllamaLLM


# --------------------------------------------------
# 1. Our engineering knowledge
# --------------------------------------------------

document = """
The Routing Service determines which fulfillment center should process an order.

The service consumes OrderCreated events from Kafka.

Kafka consumer lag can happen when consumers cannot process messages fast enough.

When troubleshooting routing issues, first check consumer lag and consumer group health.

The service also communicates with the Inventory Service to verify available inventory.

The Inventory Service checks whether sufficient stock is available before fulfillment.
"""


# --------------------------------------------------
# 2. Split document into sentences
# --------------------------------------------------

def split_sentences(text):
    return re.split(r'(?<=[.!?])\s+', text.strip())


# --------------------------------------------------
# 3. Create chunks
# --------------------------------------------------

def create_chunks(sentences, chunk_size=2, overlap=1):

    chunks = []

    start = 0

    while start < len(sentences):

        end = start + chunk_size

        chunk = sentences[start:end]

        chunks.append(" ".join(chunk))

        start = end - overlap

    return chunks


sentences = split_sentences(document)

chunks = create_chunks(sentences)


print("\nCreated chunks:")

for i, chunk in enumerate(chunks):
    print(f"\nChunk {i}:")
    print(chunk)


# --------------------------------------------------
# 4. Load embedding model
# --------------------------------------------------

embedding_model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)

embeddings = embedding_model.encode(chunks)


# --------------------------------------------------
# 5. Create Qdrant
# --------------------------------------------------

client = QdrantClient(":memory:")

collection_name = "engineering_docs"

client.create_collection(
    collection_name=collection_name,
    vectors_config=VectorParams(
        size=384,
        distance=Distance.COSINE
    )
)


# --------------------------------------------------
# 6. Store chunks in Qdrant
# --------------------------------------------------

points = []

for i, (chunk, embedding) in enumerate(
    zip(chunks, embeddings)
):

    points.append(
        PointStruct(
            id=i,
            vector=embedding.tolist(),
            payload={
                "text": chunk,
                "chunk_id": i
            }
        )
    )


client.upsert(
    collection_name=collection_name,
    points=points
)


print("\nChunks stored in Qdrant.")


# --------------------------------------------------
# 7. User question
# --------------------------------------------------

query = "Why are orders getting stuck?"


# --------------------------------------------------
# 8. Embed the question
# --------------------------------------------------

query_embedding = embedding_model.encode(query)


# --------------------------------------------------
# 9. Search Qdrant
# --------------------------------------------------

results = client.query_points(
    collection_name=collection_name,
    query=query_embedding.tolist(),
    limit=3
).points


# --------------------------------------------------
# 10. Extract retrieved text
# --------------------------------------------------

retrieved_chunks = []

for result in results:

    retrieved_chunks.append(
        result.payload["text"]
    )


print("\nRetrieved chunks:")

for chunk in retrieved_chunks:
    print("\n", chunk)


# --------------------------------------------------
# 11. Build context
# --------------------------------------------------

context = "\n\n".join(retrieved_chunks)


# --------------------------------------------------
# 12. Build LLM prompt
# --------------------------------------------------

prompt = f"""
You are an engineering support assistant.

Answer the question using only the provided context.

If the context does not contain enough information,
say that there is not enough information.

Context:
{context}

Question:
{query}

Answer:
"""


print("\nSending prompt to LLM...")


# --------------------------------------------------
# 13. Call Llama 3
# --------------------------------------------------

llm = OllamaLLM(model="llama3")

response = llm.invoke(prompt)


# --------------------------------------------------
# 14. Display final answer
# --------------------------------------------------

print("\nFinal Answer:")
print(response)