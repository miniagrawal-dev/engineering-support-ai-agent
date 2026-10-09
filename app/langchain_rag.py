from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, Filter, FieldCondition, MatchValue

from langchain_qdrant import QdrantVectorStore
from langchain_core.documents import Document
from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import OllamaLLM
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.runnables import RunnablePassthrough, RunnableParallel


# --------------------------------------------------
# 2. Create Qdrant client
# --------------------------------------------------

client = QdrantClient(":memory:")

collection_name = "engineering_docs"


# --------------------------------------------------
# 3. Create Qdrant collection
# --------------------------------------------------

client.create_collection(
    collection_name=collection_name,
    vectors_config=VectorParams(
        size=384,
        distance=Distance.COSINE
    )
)


# --------------------------------------------------
# 4. Create engineering documents
# --------------------------------------------------

documents = [

    Document(
        page_content=(
            "The Routing Service consumes OrderCreated events "
            "from Kafka."
        ),
        metadata={
            "service": "routing-service",
            "type": "architecture"
        }
    ),

    Document(
        page_content=(
            "Kafka consumer lag can happen when consumers "
            "cannot process messages fast enough."
        ),
        metadata={
            "service": "routing-service",
            "type": "runbook"
        }
    ),

    Document(
        page_content=(
            "When troubleshooting routing issues, first "
            "check consumer lag and consumer group health."
        ),
        metadata={
            "service": "routing-service",
            "type": "runbook"
        }
    ),

    Document(
        page_content=(
            "The Inventory Service checks whether sufficient "
            "stock is available before fulfillment."
        ),
        metadata={
            "service": "inventory-service",
            "type": "architecture"
        }
    )
]


# --------------------------------------------------
# 5. Adapter for SentenceTransformer
# --------------------------------------------------

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)


# --------------------------------------------------
# 6. Create LangChain Qdrant vector store
# --------------------------------------------------

vector_store = QdrantVectorStore(
    client=client,
    collection_name=collection_name,
    embedding=embeddings
)


# --------------------------------------------------
# 7. Store documents in Qdrant
# --------------------------------------------------

vector_store.add_documents(documents)


# --------------------------------------------------
# 8. Create retriever
# --------------------------------------------------

# retriever = vector_store.as_retriever(
#     search_kwargs={
#         "k": 4
#     }
# )

retriever = vector_store.as_retriever(
    search_kwargs={
        "k": 4,
        "filter": Filter(
            must=[
                FieldCondition(
                    key="metadata.service",
                    match=MatchValue(value="routing-service")
                )
            ]
        )
    }
)

# --------------------------------------------------
# 9. User question
# --------------------------------------------------

question = "Why are orders getting stuck?"


# --------------------------------------------------
# 10. Retrieve relevant documents
# --------------------------------------------------

retrieved_documents = retriever.invoke(question)


print("\nRetrieved documents:")

for document in retrieved_documents:

    print("\nContent:")
    print(document.page_content)

    print("Metadata:")
    print(document.metadata)


# --------------------------------------------------
# 11. Convert Documents into context
# --------------------------------------------------

def format_documents(documents):

    return "\n\n".join(
        document.page_content
        for document in documents
    )


context = format_documents(
    retrieved_documents
)


# --------------------------------------------------
# 12. Create prompt template
# --------------------------------------------------

prompt = ChatPromptTemplate.from_template(
    """
You are an engineering support assistant.

Answer the question using only the provided context.

If the context does not contain enough information,
say that there is not enough information.

Context:
{context}

Question:
{question}

Answer:
"""
)


# --------------------------------------------------
# 13. Create LLM
# --------------------------------------------------

llm = OllamaLLM(
    model="llama3"
)


# # 14. Create LangChain chain
# chain = prompt | llm
# # 15. Generate answer
# response = chain.invoke(
#     {
#         "context": context,
#         "question": question
#     }
# )

# rag_chain = (
#     {
#         "context": retriever | format_documents,
#         "question": RunnablePassthrough()
#     }
#     | prompt
#     | llm
# )
#
# response = rag_chain.invoke(question)


# Build the retrieval stage only
retrieval_chain = RunnableParallel({
    "context": retriever | format_documents,
    "question": RunnablePassthrough()
})
# Inspect what the retrieval stage produces
retrieval_result = retrieval_chain.invoke(question)

print("\n--- Intermediate Result ---")
print("Question:")
print(retrieval_result["question"])

print("\nRetrieved Context:")
print(retrieval_result["context"])


# Continue with the complete RAG pipeline
rag_chain = retrieval_chain | prompt | llm

response = rag_chain.invoke(question)

print("\n--- Final Answer ---")
print(response)
