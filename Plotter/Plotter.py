import json
import os
import re
import matplotlib.pyplot as plt

# Make sure filenames don't contain illegal characters for Windows
def sanitize_filename(s):
    s = s.replace('\n', ' ').strip()                # Remove newlines
    s = re.sub(r'[<>:"/\\|?*]', '_', s)             # Replace illegal characters with underscores
    s = re.sub(r'\s+', '_', s)                      # Collapse multiple spaces
    return s

# Ensure output directory exists
os.makedirs("plots", exist_ok=True)

# Load the JSON data
with open("subjects_output.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# Iterate over all subjects and tasks
for subject_id, subject in data.items():
    tasks = subject.get("Tasks", {})
    for task_name, labels in tasks.items():
        for label, entries in labels.items():
            x_vals = [e["X"] for e in entries if "X" in e]
            y_vals = [e["Y"] for e in entries if "Y" in e]

            # Skip plots with no coordinates
            if not x_vals or not y_vals:
                continue

            # Plot the data
            plt.figure()
            plt.scatter(x_vals, y_vals, label=label)
            plt.title(f"{subject_id} - {task_name} - {label}")
            plt.xlabel("X")
            plt.ylabel("Y")
            plt.legend()

            # Create sanitized filename
            safe_subject = sanitize_filename(subject_id)
            safe_task = sanitize_filename(task_name)
            safe_label = sanitize_filename(label)
            filename = f"plots/{safe_subject}_{safe_task}_{safe_label}.png"

            # Save and close the figure
            plt.savefig(filename)
            plt.close()
