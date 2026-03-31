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
from prompts.prompt_3 import prompt_3
from values.activities import activities 

load_dotenv()

api_key = os.getenv("GOOGLE_API_KEY")

client = genai.Client(api_key=api_key)

results_dir = Path("../../results/gemini/gemini_flash_2.5_temp_0")
excel_path = results_dir / "gemini_sheet_results.xlsx"
timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')

results_dir.mkdir(exist_ok=True)
output_path = results_dir / f"gemini_grouped_activities_by_dimension_{timestamp}.xlsx"

xls = pd.ExcelFile(excel_path)
sheet_names = xls.sheet_names

dimension_sheets = [s for s in sheet_names if s not in ['Dimensions', 'Dimension']]

results = {}

for sheet in dimension_sheets:
    print(f"Processing sheet: {sheet}")

    df = pd.read_excel(excel_path, sheet_name=sheet)
    sheet_activities = df.iloc[:, 0].dropna().tolist()

    prompt = prompt_3.format(
        dimension=sheet,
        activities="\n".join(f"- {a}" for a in sheet_activities)
    )

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
        config=types.GenerateContentConfig(
            system_instruction="Output ONLY a Markdown table. Do not include any introductory or concluding text.",
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

    parsed = [row for row in parsed if len(row) == 3]

    if len(parsed) < 2:
        print(f"Warning: No valid table rows found for sheet '{sheet}'. Raw response:\n{answer}\n")
        results[sheet] = pd.DataFrame(columns=["Proposed Activity Name", "Grouped Activities", "A brief explanation"])
        continue

    df_result = pd.DataFrame(parsed[1:], columns=parsed[0])
    results[sheet] = df_result
    print(f"  -> {len(df_result)} rows parsed successfully.")

with pd.ExcelWriter(output_path, engine="openpyxl") as writer:
    for sheet_name, df_sheet in results.items():
        df_sheet.to_excel(writer, sheet_name=sheet_name[:31], index=False)

print(f"\nResults saved to: {output_path}")