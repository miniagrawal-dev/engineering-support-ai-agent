from sentence_transformers import SentenceTransformer
import numpy as np

model = SentenceTransformer("all-MiniLM-L6-v2")

sentences = [
    "Java developer with Kafka experience",
    "Backend engineer experienced in Kafka",
    "I love eating pizza"
]

embeddings = model.encode(sentences)

# for sentence, embedding in zip(sentences, embeddings):
#     print(sentence)
#     print("Vector dimensions:", len(embedding))
#     print("First 10 values:", embedding[:10])
#     print()

def cosine_similarity(vector_a, vector_b) :
     dot_product = np.dot(vector_a, vector_b)

     magnitude_a = np.linalg.norm(vector_a)
     magnitude_b = np.linalg.norm(vector_b)

     return dot_product / (magnitude_a * magnitude_b)


similarity_01 = cosine_similarity(embeddings[0], embeddings[1])
similarity_02 = cosine_similarity(embeddings[0], embeddings[2])
similarity_12 = cosine_similarity(embeddings[1], embeddings[2])

print("Java/Kafka ↔ Backend/Kafka:", similarity_01)
print("Java/Kafka ↔ Pizza:", similarity_02)
print("Backend/Kafka ↔ Pizza:", similarity_12)