import json
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter


with open("parsed_pages.json", "r", encoding="utf-8") as f:
    pages = json.load(f)


documents = []

for page in pages:
    doc = Document(
        page_content=page["text"],
        metadata={
            "paper_id": page["paper_id"],
            "page_number": page["page_number"],
            "source": page["source"]
        }
    )
    documents.append(doc)


splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200
)

chunks = splitter.split_documents(documents)

formatted = []
for i, chunk in enumerate(chunks):
    meta = chunk.metadata
    formatted.append({
        "chunk_id": f"{meta['paper_id']}_p{meta['page_number']}_c{i}",
        "content": chunk.page_content,
        "metadata": {
            "paper_id": meta['paper_id'],
            "page_number": meta['page_number'],
            "source": meta['source'],
            "chunk_index": i
        }
    })

with open("parsed_chunks.json", "w", encoding="utf-8") as f:
    json.dump(formatted, f, indent=2, ensure_ascii=False)

print(f"Saved {len(formatted)} chunks to parsed_chunks.json")