import json
import faiss
import sys
from openai import OpenAI
from datetime import datetime
from pathlib import Path
import numpy as np
import os
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

index = faiss.read_index("faiss_index.index")

with open("parsed_chunks.json", "r", encoding="utf-8") as f:
    chunks = json.load(f)

actors = [
    "Business Stakeholder",
    "Solution Architect",
    "Domain Expert",
    "Manager",
    "Data Scientist",
    "Data Engineer",
    "Data Steward",
    "Scientist",
    "ML Engineer / Developer",
    "Software Developer",
    "Software Engineer",
    "Application Developer",
    "DevOps Engineer",
    "MLOps Engineer",
    "Operations Engineer",
    "IT Operations / Professional"
]

query = """You're an expert in machine learning operations (MLOps). 
You will find below a list that contains 16 Actors who appear in different activities in an MLOps process. 

I want you to:
• Identify dimensions from the provided actors.
• Cluster actors according to these dimensions.
• Propose a leading actor for each dimension.

Format the final output as a structured table with three columns: Dimension, List of Actors, Proposed Leading Actor.

Here is the list of actors:
""" + "\n".join([f"- {actor}" for actor in actors])


query_response = client.embeddings.create(
    input=[query],
    model="text-embedding-3-small"
)
query_embedding = np.array([query_response.data[0].embedding], dtype=np.float32)

k = 50
distances, indices = index.search(query_embedding, k)

for i, idx in enumerate(indices[0]):
    print(f"\n--- Result {i+1} ---")
    print("Distance:", distances[0][i])
    print("Chunk content:", chunks[idx]["content"][:500], "...") 


retrieved = []
for i, idx in enumerate(indices[0]):
    retrieved.append({
        "rank": i + 1,
        "distance": float(distances[0][i]),
        "content": chunks[idx]["content"],
        "metadata": chunks[idx]["metadata"]
    })


joined_chunks = "\n\n".join([chunk["content"] for chunk in retrieved])
final_prompt = f"""You are a helpful assistant for MLOps tasks.

Your job is to answer the question using ONLY the context provided between the --- markers.


---
{joined_chunks}
---

Question: {query}
Answer:"""


Path("retrieved_contexts").mkdir(exist_ok=True)

snapshot = {
    "query": query,
    "retrieved_chunks": retrieved,
    "final_prompt": final_prompt
}

filename = f"retrieved_contexts/query_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
with open(filename, "w", encoding="utf-8") as f:
    json.dump(snapshot, f, ensure_ascii=False, indent=2)

print(f"\nSaved query and retrieved chunks to: {filename}")