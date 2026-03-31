import json
from pathlib import Path
import pandas as pd
import re
import os
from dotenv import load_dotenv
from google.genai import types
import google.genai as genai
from datetime import datetime
load_dotenv()

api_key = os.getenv("GOOGLE_API_KEY")

client = genai.Client(api_key=api_key)

context_dir = Path("retrieved_contexts")
latest_file = max(context_dir.glob("query_*.json"), key=lambda f: f.stat().st_mtime)

with open(latest_file, "r", encoding="utf-8") as f:
    data = json.load(f)

prompt = data["final_prompt"]


response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents=prompt,
    config=types.GenerateContentConfig(
        temperature=0,
        thinking_config=types.ThinkingConfig(include_thoughts=False, thinking_budget=0)
    ),
)
answer = response.text.strip()

print(f"\n Query: {data['query']}")
print("\n Retrieved Context Summary:")
for i, chunk in enumerate(data["retrieved_chunks"], 1):
    print(f"  {i}. Source: {chunk['metadata']['source']} (page {chunk['metadata']['page_number']})")

print("\n Model Answer:")
print(answer)

text_output_path = context_dir / "model_results.txt"
with open(text_output_path, "w", encoding="utf-8") as f:
    f.write(answer)
print(f"Saved plain text to {text_output_path}")

lines = [line.strip() for line in answer.split("\n") if line.strip()]
markdown_table_lines = [line for line in lines if line.startswith("|") and "|" in line]
markdown_table_lines = [line for line in markdown_table_lines if not re.match(r"^\|\s*-", line)]

if markdown_table_lines:
    parsed = [[cell.strip() for cell in line.split("|")[1:-1]] for line in markdown_table_lines]
    df = pd.DataFrame(parsed[1:], columns=["Activity", "Dimension"] if len(parsed[0]) == 2 else parsed[0])
elif any(" | " in line for line in lines):
    loose_rows = [line for line in lines if " | " in line and "Dimension" not in line]
    parsed = [line.split(" | ") for line in loose_rows]
    df = pd.DataFrame(parsed, columns=["Dimension", "List of Actors", "Proposed Leading Actor"])
else:
    df = None

results_dir = Path("results/gemini/gemini_flash_2.5_temp_0")
results_dir.mkdir(exist_ok=True)
timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')

if df is not None and not df.empty:
    excel_output_path = results_dir / f"prompt_gemini_2.5_flash_{timestamp}_results.xlsx"
    df.to_excel(excel_output_path, index=False)
    print(f"Saved Excel table to {excel_output_path}")
else:
    print("No table detected to export to Excel.")
