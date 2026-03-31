import pandas as pd
import re
from pathlib import Path
import anthropic
from anthropic import Anthropic
import os
import sys
from dotenv import load_dotenv
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent.parent))

from prompts.prompt_1 import prompt_1
from values.query import query
from values.activities import activities 
from values.actors import actors

load_dotenv()

api_key = os.getenv("ANTHROPIC_API_KEY")

client = Anthropic(api_key=api_key)


formatted_query = query.format(
    actors=", ".join(actors),
)

response = client.messages.create(
    model="claude-sonnet-4-6",
    messages=[{"role": "user", "content": prompt_1.format( query=formatted_query)}],
    temperature=0,
    max_tokens=4096

)
answer = response.content[0].text.strip()
print(answer)

text_output = Path("../text_outputs/anthropic/claude_sonnet_temp_0")
text_output_path = text_output / "claude_sonnet_temp_0_model_results.txt"

with open(text_output_path, "w", encoding="utf-8") as f:
    f.write(answer)
print(f"saved plain text to {text_output_path} ")

lines = [line.strip() for line in answer.split("\n") if line.strip() ]
markdown_table_lines = [line for line in lines if line.startswith("|") and "|" in line ]
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

results_dir = Path("../results/anthropic/claude_sonnet_temp_0")
timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')

if df is not None and not df.empty:
    try:
        excel_output_path = results_dir / f"claude_sonnet_temp_0_model_results_{timestamp}.xlsx"
        df.to_excel(excel_output_path, index=False)
        print(f"Saved Excel table to {excel_output_path}")
    except PermissionError:
        print(f"Permission denied: Close the Excel file if it's open and try again")
    except ImportError:
        print("(openpyxl not installed, skipping Excel export)")
else:
    print("No table detected to export to Excel.")
