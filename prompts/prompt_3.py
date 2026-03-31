prompt_3 = """You're an expert in machine learning operations (MLOps). You will find, at the end, a list of activities related to the "{dimension}" Dimension. You are asked to:
• Group similar activities and propose new activity name. The proposed activity name should start with a verb. Use concise verb phrase, for example I prefer "Review Code" instead of "perform code review".
• Ensure activities are not mistakenly merged if they represent distinct tasks.
• Format the final output as a structured table with three columns: Proposed Activity Name, Grouped Activities, A brief explanation. Order the activities in the table in a chronological order.

Activities:
{activities}

Now produce the final table:
| Proposed Activity Name | Grouped Activities | A brief explanation |
| --- | --- | --- |"""