prompt_2 = """You're an expert in machine learning operations (MLOps).

You are given a list of 402 activities that appear in different MLOps processes.

Your task:
1. Assign each dimension to exactly one of the below given activities.
2. Do not group activities together — each row must correspond to one activity only.
3. The final output must be a Markdown table with EXACTLY 403 rows (including the headers: Activity | Dimension).
4. The table must have exactly two columns: 'Activity' and 'Dimension'.
5. Ensure that activities are not mistakenly categorized.

These are the dimensions, do not add dimensions on your own, refer only to these:
{dimensions}

These are the activities:
{activities}

Now produce the final Markdown table:

| Activity | Dimension |
| --- | --- |"""
