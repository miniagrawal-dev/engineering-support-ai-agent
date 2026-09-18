import re

from sentence_transformers import SentenceTransformer

from qdrant_client import QdrantClient
from qdrant_client.models import (
    Distance,
    PointStruct,
    VectorParams
)


document = """
The Routing Service determines which fulfillment center should process an order.

The service consumes OrderCreated events from Kafka.

Kafka consumer lag can happen when consumers cannot process messages fast enough.

When troubleshooting routing issues, first check consumer lag and consumer group health.

The service also communicates with the Inventory Service to verify available inventory.

The Inventory Service checks whether sufficient stock is available before fulfillment.
"""


# --------------------------------------------------
# Step 1: Split document into sentences
# --------------------------------------------------

def split_sentences(text):
    return re.split(r'(?<=[.!?])\s+', text.strip())


# --------------------------------------------------
# Step 2: Create chunks with overlap
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

chunks = create_chunks(
    sentences,
    chunk_size=2,
    overlap=1
)


print("Created chunks:")

for i, chunk in enumerate(chunks):
    print(f"\nChunk {i}:")
    print(chunk)


# --------------------------------------------------
# Step 3: Create embeddings
# --------------------------------------------------

model = SentenceTransformer("all-MiniLM-L6-v2")

embeddings = model.encode(chunks)

print("\nEmbedding shape:")
print(embeddings.shape)


# --------------------------------------------------
# Step 4: Create Qdrant collection
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
# Step 5: Store vectors + text in Qdrant
# --------------------------------------------------

points = []

for i, (chunk, embedding) in enumerate(zip(chunks, embeddings)):

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


print("\nStored chunks in Qdrant.")


# --------------------------------------------------
# Step 6: User question
# --------------------------------------------------

query = "Why are orders getting stuck?"


# --------------------------------------------------
# Step 7: Convert question into embedding
# --------------------------------------------------

query_embedding = model.encode(query)


# --------------------------------------------------
# Step 8: Search Qdrant
# --------------------------------------------------

results = client.query_points(
    collection_name=collection_name,
    query=query_embedding.tolist(),
    limit=3
).points


# --------------------------------------------------
# Step 9: Display results
# --------------------------------------------------

print("\nSearch results:")

for result in results:

    print(f"\nScore: {result.score:.4f}")

    print("Chunk:")
    print(result.payload["text"])