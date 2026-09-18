import re

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


def split_sentences(text):
    sentences = re.split(r'(?<=[.!?])\s+', text.strip())
    return sentences


sentences = split_sentences(document)

for i, sentence in enumerate(sentences):
    print(f"{i}: {sentence}")