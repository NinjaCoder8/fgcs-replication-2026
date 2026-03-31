import json
from openai import OpenAI
import faiss
import numpy as np
from tqdm import tqdm
import os
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

with open("parsed_chunks.json", "r", encoding="utf-8") as f:
    chunks = json.load(f)

texts = [chunk["content"] for chunk in chunks]

embeddings_list = []
batch_size = 100
for i in tqdm(range(0, len(texts), batch_size), desc="Getting embeddings from OpenAI"):
    batch = texts[i:i+batch_size]
    response = client.embeddings.create(
        input=batch,
        model="text-embedding-3-small"
    )
    for item in response.data:
        embeddings_list.append(item.embedding)

embeddings = np.array(embeddings_list, dtype=np.float32)

dimension = embeddings.shape[1]
index = faiss.IndexFlatL2(dimension) 
index.add(embeddings) 


faiss.write_index(index, "faiss_index.index")

print(f"FAISS index saved with {len(chunks)} vectors")
