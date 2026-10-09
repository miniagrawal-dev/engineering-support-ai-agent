from langchain_ollama import OllamaLLM


llm = OllamaLLM(model="llama3")

response = llm.invoke(
    "Explain Kafka consumer lag in 3 sentences."
)

print(response)