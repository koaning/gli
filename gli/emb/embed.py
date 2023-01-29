import pandas as pd

# pip install -U sentence-transformers
from sentence_transformers import SentenceTransformer
from umap import UMAP

# Load the universal sentence encoder
model = SentenceTransformer("paraphrase-MiniLM-L6-v2")

# Load original dataset
df = pd.read_csv("dataset.csv")[["text"]]
sentences = df["text"]

# Calculate embeddings
X = model.encode(sentences)

# Reduce the dimensions with UMAP
umap = UMAP()
X_tfm = umap.fit_transform(X)

# Apply coordinates
df["x"] = X_tfm[:, 0]
df["y"] = X_tfm[:, 1]

df.to_csv("ready.csv")
