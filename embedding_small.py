from sentence_transformers import SentenceTransformer

model = SentenceTransformer("BAAI/bge-small-en-v1.5")

text = """
Transformers are neural networks that use self-attention
to understand relationships between words.
"""

embedding = model.encode(text)

print(embedding.shape)