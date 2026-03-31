import pandas as pd
import re
from pathlib import Path
from google import genai
from google.genai import types
import os
import sys
from dotenv import load_dotenv
from datetime import datetime
import time

sys.path.insert(0, str(Path(__file__).parent.parent))

from prompts.prompt_1 import prompt_1
from values.query import query
from values.activities import activities 
from values.actors import actors

load_dotenv()

api_key = os.getenv("GOOGLE_API_KEY")

client = genai.Client(api_key=api_key)

formatted_query = query.format(
    actors=", ".join(actors),
)

response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents=prompt_1.format(query=formatted_query),
    config=types.GenerateContentConfig(
        system_instruction="Output ONLY a Markdown table. Do not include any introductory or concluding text.",
        temperature=0,
    ),
)

answer = response.text.strip()
print(answer)

text_output = Path("../text_outputs/gemini/gemini_flash_2.5_temp_0")
text_output.mkdir(parents=True, exist_ok=True)
text_output_path = text_output / "gemini_flash_2.5_temp_0_model_results.txt"

with open(text_output_path, "w", encoding="utf-8") as f:
    f.write(answer)
print(f"Saved plain text to {text_output_path}")

lines = [line.strip() for line in answer.split("\n") if line.strip()]
markdown_table_lines = [line for line in lines if line.startswith("|") and "|" in line]
markdown_table_lines = [line for line in markdown_table_lines if not re.match(r"^\|\s*-", line)]

df = None
if markdown_table_lines:
    parsed = [[cell.strip() for cell in line.split("|")[1:-1]] for line in markdown_table_lines]
    headers = parsed[0]
    rows = [row for row in parsed[1:] if len(row) == len(headers)]
    df = pd.DataFrame(rows, columns=headers)
elif any(" | " in line for line in lines):
    loose_rows = [line for line in lines if " | " in line and "Dimension" not in line]
    parsed = [line.split(" | ") for line in loose_rows]
    df = pd.DataFrame(parsed, columns=["Dimension", "List of Actors", "Proposed Leading Actor"])

results_dir = Path("../results/gemini/gemini_flash_2.5_temp_0")
results_dir.mkdir(parents=True, exist_ok=True)
timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')

if df is not None and not df.empty:
    try:
        excel_output_path = results_dir / f"gemini_flash_2.5_temp_0_model_results_{timestamp}.xlsx"
        df.to_excel(excel_output_path, index=False)
        print(f"Saved Excel table to {excel_output_path}")
    except PermissionError:
        print("Permission denied: Close the Excel file if it's open and try again")
    except ImportError:
        print("(openpyxl not installed, skipping Excel export)")
else:
    print("No table detected to export to Excel.")