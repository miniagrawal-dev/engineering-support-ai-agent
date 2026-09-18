from sentence_transformers import SentenceTransformer
import numpy as np


model = SentenceTransformer("all-MiniLM-L6-v2")


documents = [
    "Kafka consumer lag can happen when consumers cannot process messages fast enough.",
    "The routing service consumes order events from the Kafka topic.",
    "Redis is used to cache frequently accessed order information.",
    "The inventory service checks available stock before fulfillment.",
    "Kubernetes restarts pods when their liveness probe fails."
]


#query = "Why is the routing service not processing orders?"
query = "Messages are getting stuck because consumers are slow."


document_embeddings = model.encode(documents)
query_embedding = model.encode(query)


def cosine_similarity(vector_a, vector_b):
    dot_product = np.dot(vector_a, vector_b)

    magnitude_a = np.linalg.norm(vector_a)
    magnitude_b = np.linalg.norm(vector_b)

    return dot_product / (magnitude_a * magnitude_b)


results = []

for document, embedding in zip(documents, document_embeddings):
    score = cosine_similarity(query_embedding, embedding)
    results.append((score, document))


results.sort(reverse=True)


print("Query:")
print(query)
print("\nSearch results:\n")

for score, document in results:
    print(f"{score:.4f} -> {document}")