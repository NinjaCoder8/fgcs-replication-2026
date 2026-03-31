import faiss
import numpy as np

index = faiss.read_index("faiss_index.index")

print(f"Number of vectors in FAISS: {index.ntotal}")
print(f"Vector dimension: {index.d}\n")

for i in range(index.ntotal):
    vector = index.reconstruct(i) 
    print(f"Vector {i} (first 10 values): {vector[:10]}") 
