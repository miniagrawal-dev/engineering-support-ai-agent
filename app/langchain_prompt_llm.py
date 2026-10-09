from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import OllamaLLM


prompt = ChatPromptTemplate.from_template(
    """
You are an engineering support assistant.

Answer the question using only the provided context.

Context:
{context}

Question:
{question}

Answer:
"""
)


llm = OllamaLLM(model="llama3")


chain = prompt | llm


response = chain.invoke({
    "context": """
Kafka consumer lag can happen when consumers cannot
process messages fast enough.

When troubleshooting routing issues, first check
consumer lag and consumer group health.
""",
    "question": "Why are orders getting stuck?"
})


print(response)