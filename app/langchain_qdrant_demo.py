from sentence_transformers import SentenceTransformer

from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams

from langchain_qdrant import QdrantVectorStore
from langchain_core.documents import Document


# --------------------------------------------------
# Embedding model
# --------------------------------------------------

embedding_model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)


# --------------------------------------------------
# Qdrant
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
# Documents
# --------------------------------------------------

documents = [

    Document(
        page_content="The Routing Service consumes OrderCreated events from Kafka.",
        metadata={
            "service": "routing-service",
            "type": "architecture"
        }
    ),

    Document(
        page_content="Kafka consumer lag can happen when consumers cannot process messages fast enough.",
        metadata={
            "service": "routing-service",
            "type": "runbook"
        }
    ),

    Document(
        page_content="The Inventory Service checks whether sufficient stock is available before fulfillment.",
        metadata={
            "service": "inventory-service",
            "type": "architecture"
        }
    )
]


# --------------------------------------------------
# Adapter for SentenceTransformer
# --------------------------------------------------

class SentenceTransformerEmbeddings:

    def __init__(self, model):
        self.model = model

    def embed_documents(self, texts):
        return self.model.encode(texts).tolist()

    def embed_query(self, text):
        return self.model.encode(text).tolist()


embeddings = SentenceTransformerEmbeddings(
    embedding_model
)


# --------------------------------------------------
# LangChain Qdrant vector store
# --------------------------------------------------

vector_store = QdrantVectorStore(
    client=client,
    collection_name=collection_name,
    embedding=embeddings
)


# --------------------------------------------------
# Store documents
# --------------------------------------------------

vector_store.add_documents(documents)


# --------------------------------------------------
# Retriever
# --------------------------------------------------

retriever = vector_store.as_retriever(
    search_kwargs={
        "k": 2
    }
)


# --------------------------------------------------
# Search
# --------------------------------------------------

query = "Why are orders getting stuck?"

results = retriever.invoke(query)


# --------------------------------------------------
# Display results
# --------------------------------------------------

print("\nRetrieved documents:")

for result in results:

    print("\nContent:")
    print(result.page_content)

    print("Metadata:")
    print(result.metadata)