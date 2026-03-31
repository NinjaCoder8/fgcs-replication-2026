import json
import pandas as pd
import re
from pathlib import Path
from google import genai
from google.genai import types
import os
from dotenv import load_dotenv
from datetime import datetime 
import sys

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from values.activities import activities 
from prompts.prompt_2 import prompt_2

load_dotenv()

api_key = os.getenv("GOOGLE_API_KEY")

client = genai.Client(api_key=api_key)

results_dir = Path("../../results/gemini/gemini_flash_2.5_temp_0")
df = pd.read_excel(results_dir / "gemini_flash_2.5_temp_0_model_results_20260319_201812.xlsx")
dimensions = df["Dimension"].tolist()

prompt = prompt_2.format(
    dimensions="\n".join(dimensions),
    activities="\n".join(activities)
)

system_instruction="Output ONLY a Markdown table. Do not include any introductory or concluding text.",

response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents=prompt,
    config=types.GenerateContentConfig(
        system_instruction=system_instruction,
        temperature=0,
    ),
)

answer = response.text.strip()

lines = [line.strip() for line in answer.split("\n") if line.strip()]
table_lines = [line for line in lines if line.startswith("|") and not re.match(r"^\|\s*-", line)]

parsed = []
for line in table_lines:
    cells = [c.strip() for c in line.split("|")[1:-1]]
    parsed.append(cells)

timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
df = pd.DataFrame(parsed, columns=["Activity", "Dimension"])
output_path = results_dir / f"prompt_02_gemini_results_{timestamp}.xlsx"

df.to_excel(output_path, index=False)
print(f"Results saved to {output_path}")
