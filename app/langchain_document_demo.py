from langchain_core.documents import Document


document = Document(
    page_content="Kafka consumer lag can happen when consumers cannot process messages fast enough.",
    metadata={
        "service": "routing-service",
        "type": "runbook"
    }
)


print("Content:")
print(document.page_content)

print("\nMetadata:")
print(document.metadata)