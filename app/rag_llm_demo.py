from langchain_ollama import OllamaLLM

query = "Why are orders getting stuck?"

retrieved_chunks = [
    "The service consumes OrderCreated events from Kafka.",
    "Kafka consumer lag can happen when consumers cannot process messages fast enough.",
    "When troubleshooting routing issues, first check consumer lag and consumer group health."
]


context = "\n\n".join(retrieved_chunks)


prompt = f"""
You are an engineering support assistant.

Answer the user's question using only the provided context.

Context:
{context}

Question:
{query}

Answer:
"""


llm = OllamaLLM(model="llama3")

response = llm.invoke(prompt)

print(response)