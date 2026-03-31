from pathlib import Path
import pandas as pd

results_dir = Path("../results/gemini/gemini_flash_2.5_temp_0")
prompt_01_file = results_dir / "gemini_flash_2.5_temp_0_model_results_20260319_201812.xlsx"
prompt_02_file = results_dir / "prompt_02_gemini_results.xlsx"
output_file = results_dir / "gemini_sheet_results.xlsx"

df_dimensions = pd.read_excel(prompt_01_file)
df_activities = pd.read_excel(prompt_02_file)

with pd.ExcelWriter(output_file, engine="openpyxl") as writer:

    df_dimensions.to_excel(writer, sheet_name="Dimensions", index=False)
    
    for dim in df_activities["Dimension"].unique():
        filtered = df_activities[df_activities["Dimension"] == dim]
        safe_sheet_name = dim[:31].replace("/", "-").replace("\\", "-")
        filtered.to_excel(writer, sheet_name=safe_sheet_name, index=False)

print(f"Combined Excel file saved to {output_file}")
