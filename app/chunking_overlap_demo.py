import re


document = """
The Routing Service determines which fulfillment center should process an order.

The service consumes OrderCreated events from Kafka.

Kafka consumer lag can happen when consumers cannot process messages fast enough.

When troubleshooting routing issues, first check consumer lag and consumer group health.

The service also communicates with the Inventory Service to verify available inventory.

The Inventory Service checks whether sufficient stock is available before fulfillment.
"""


def split_sentences(text):
    return re.split(r'(?<=[.!?])\s+', text.strip())


def create_chunks(sentences, chunk_size=2, overlap=1):
    chunks = []

    start = 0

    while start < len(sentences):

        end = start + chunk_size

        chunk = sentences[start:end]

        chunks.append(" ".join(chunk))

        start = end - overlap

    return chunks


sentences = split_sentences(document)

chunks = create_chunks(
    sentences,
    chunk_size=2,
    overlap=1
)


for i, chunk in enumerate(chunks):
    print(f"\n--- Chunk {i} ---")
    print(chunk)