from sentence_transformers import SentenceTransformer
import faiss
import numpy as np


model = SentenceTransformer("all-MiniLM-L6-v2")


documents = [
    "Kafka consumer lag can happen when consumers cannot process messages fast enough.",
    "The routing service consumes order events from the Kafka topic.",
    "Redis is used to cache frequently accessed order information.",
    "The inventory service checks available stock before fulfillment.",
    "Kubernetes restarts pods when their liveness probe fails."
]


query = "Messages are getting stuck because consumers are slow."


# Create embeddings
document_embeddings = model.encode(documents)

# Convert to float32 because FAISS expects this format
document_embeddings = np.array(
    document_embeddings,
    dtype="float32"
)

query_embedding = model.encode([query])
query_embedding = np.array(
    query_embedding,
    dtype="float32"
)


# Create FAISS index
dimension = document_embeddings.shape[1]

index = faiss.IndexFlatIP(dimension)

# Add document vectors to the index
index.add(document_embeddings)


# Search for top 3 results
k = 3

scores, indices = index.search(query_embedding, k)


print("Query:")
print(query)

print("\nTop results:\n")

for score, index_position in zip(scores[0], indices[0]):
    print(f"{score:.4f} -> {documents[index_position]}")