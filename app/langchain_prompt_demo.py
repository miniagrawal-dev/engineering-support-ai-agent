from langchain_core.prompts import ChatPromptTemplate


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


formatted_prompt = prompt.invoke({
    "context": "Kafka consumer lag can happen when consumers cannot process messages fast enough.",
    "question": "Why are orders getting stuck?"
})


print(formatted_prompt)