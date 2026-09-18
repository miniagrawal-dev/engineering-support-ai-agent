document = """
The Routing Service determines which fulfillment center
should process an order.

The service consumes OrderCreated events from Kafka.

Kafka consumer lag can happen when consumers cannot
process messages fast enough.

When troubleshooting routing issues, first check
consumer lag and consumer group health.

The service also communicates with the Inventory Service
to verify available inventory.
"""

def chunk_text(text, chunk_size=150):
    chunks = []

    start = 0

    while start < len(text):
        end = start + chunk_size

        chunk = text[start:end]

        chunks.append(chunk.strip())

        start = end

    return chunks

chunks = chunk_text(document)

for i, chunk in enumerate(chunks):
    print(f"\n--- Chunk {i} ---")
    print(chunk)

# python app/chunking_demo.py (issue sentence cut in half)
#
# --- Chunk 0 ---
# The Routing Service determines which fulfillment center
# should process an order.
#
# The service consumes OrderCreated events from Kafka.
#
# Kafka consume
#
# --- Chunk 1 ---
# r lag can happen when consumers cannot
# process messages fast enough.
#
# When troubleshooting routing issues, first check
# consumer lag and consumer group
#
# --- Chunk 2 ---
# health.
#
# The service also communicates with the Inventory Service
# to verify available inventory.