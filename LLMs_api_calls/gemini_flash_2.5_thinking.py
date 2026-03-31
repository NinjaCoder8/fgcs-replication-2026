import pandas as pd
import re
import os
import sys
import io
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv
from google import genai
from google.genai import types

sys.path.insert(0, str(Path(__file__).parent.parent))
from prompts.prompt_1 import prompt_1
from values.query import query
from values.actors import actors


load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")
client = genai.Client(api_key=api_key)

formatted_query = query.format(actors=", ".join(actors))

response = client.models.generate_content(
    model="gemini-2.5-flash", 
    contents=prompt_1.format(query=formatted_query),
    config=types.GenerateContentConfig(
        temperature=1,
        thinking_config=types.ThinkingConfig(
            include_thoughts=False, 
        ),
        max_output_tokens=4000,
    ),
)

answer = ""
for part in response.candidates[0].content.parts:
    if hasattr(part, 'thought') and part.thought:
        continue
    if part.text:
        answer += part.text

answer = answer.strip()
print("\n--- Model Response Output ---\n")
print(answer)

text_output = Path("../text_outputs/gemini/gemini_flash_2.5_thinking")
text_output.mkdir(parents=True, exist_ok=True)
text_output_path = text_output / "gemini_flash_2.5_thinking_model_results.txt"

with open(text_output_path, "w", encoding="utf-8") as f:
    f.write(answer)
print(f"\nSaved plain text to {text_output_path}")

df = None
if "|" in answer:
    table_lines = [line.strip() for line in answer.split('\n') if '|' in line]
    table_string = "\n".join(table_lines)
    raw_data = io.StringIO(table_string)
    df = pd.read_table(raw_data, sep="|", skipinitialspace=True, engine='python')
    df = df.dropna(axis=1, how='all')
    df = df[~df.iloc[:, 0].astype(str).str.contains(r'^-+$', na=False)]
    df.columns = [str(c).strip() for c in df.columns]
    df = df.map(lambda x: str(x).replace('**', '').strip() if isinstance(x, str) else x)


results_dir = Path("../results/gemini/gemini_flash_2.5_thinking")
results_dir.mkdir(parents=True, exist_ok=True)
timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')

if df is not None and not df.empty:
    try:
        excel_output_path = results_dir / f"gemini_flash_2.5_thinking_model_results_{timestamp}.xlsx"
        df.to_excel(excel_output_path, index=False)
        print(f"Saved Excel table to {excel_output_path}")
    except PermissionError:
        print("Permission denied: Close the Excel file if it's open and try again.")
    except ImportError:
        print("(openpyxl not installed, skipping Excel export)")
else:
    print("No table detected to export to Excel.")