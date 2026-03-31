import os
import json
from langchain_community.document_loaders import PyPDFLoader

pdf_dir = "./articles"
output_file = "parsed_pages.json"
all_pages = []

for filename in os.listdir(pdf_dir):
    if filename.endswith(".pdf"):
        paper_id = os.path.splitext(filename)[0]
        print(f"Parsing: {filename}")
        
        loader = PyPDFLoader(os.path.join(pdf_dir, filename))
        pages = loader.load()
        
        for i, page in enumerate(pages):
            page_dict = {
                "paper_id": paper_id,
                "page_number": i + 1,
                "text": page.page_content,
                "source": os.path.join(pdf_dir, filename)
            }
            all_pages.append(page_dict)

with open(output_file, "w", encoding="utf-8") as f:
    json.dump(all_pages, f, indent=2, ensure_ascii=False)

print(f"Saved {len(all_pages)} pages to {output_file}")