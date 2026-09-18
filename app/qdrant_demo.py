from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct, VectorParams, Distance


model = SentenceTransformer("all-MiniLM-L6-v2")


documents = [
    "Kafka consumer lag can happen when consumers cannot process messages fast enough.",
    "The routing service consumes order events from the Kafka topic.",
    "Redis is used to cache frequently accessed order information.",
    "The inventory service checks available stock before fulfillment.",
    "Kubernetes restarts pods when their liveness probe fails."
]


# Create embeddings
embeddings = model.encode(documents)


# Create an in-memory Qdrant database
client = QdrantClient(":memory:")


# Create a collection
client.create_collection(
    collection_name="engineering_docs",
    vectors_config=VectorParams(
        size=384,
        distance=Distance.COSINE
    )
)


# Store vectors + metadata
points = []

for i, (document, embedding) in enumerate(zip(documents, embeddings)):

    points.append(
        PointStruct(
            id=i,
            vector=embedding.tolist(),
            payload={
                "text": document
            }
        )
    )


client.upsert(
    collection_name="engineering_docs",
    points=points
)


# Query
query = "Messages are getting stuck because consumers are slow."

query_embedding = model.encode(query)


results = client.query_points(
    collection_name="engineering_docs",
    query=query_embedding.tolist(),
    limit=3
).points


print("Query:")
print(query)

print("\nResults:\n")

for result in results:
    print(
        f"{result.score:.4f} -> "
        f"{result.payload['text']}"
    )