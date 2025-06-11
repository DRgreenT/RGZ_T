import json
import os
import re
import matplotlib.pyplot as plt
import matplotlib.patches as patches

# Makes sure filenames don't contain illegal characters for Windows
def sanitize_filename(s):
    s = s.replace('\n', ' ').strip()
    s = re.sub(r'[<>:"/\\|?*]', '_', s)
    s = re.sub(r'\s+', '_', s)
    return s

# Json file path
path = "C:\\Users\\thoma\\source\\repos\\_projects\\RGZ_T\\bin\\Debug\\net9.0\\"

# Ensure output directory exists
os.makedirs(path + "plots", exist_ok=True)

# Load the JSON data
json_path = path + "subjects_output.json"
print(f"Loading data from {json_path}...")
with open(json_path, "r", encoding="utf-8") as f:
    data = json.load(f)

print(f"Loaded {len(data)} subjects.")

# Iterate over all subjects and tasks
for subject_index, (subject_id, subject) in enumerate(data.items(), start=1):
    tasks = subject.get("Tasks", {})

    print(f"[{subject_index}/{len(data)}] Processing subject {subject_id} with {len(tasks)} tasks...")

    for task_name, labels in tasks.items():
        for label, entries in labels.items():

            if len(entries) < 3:
                continue

            x_vals = [e["X"] for e in entries if "X" in e]
            y_vals = [e["Y"] for e in entries if "Y" in e]

            # Skip plots with no coordinates
            if not x_vals or not y_vals:
                print(f"  Skipping empty plot: {subject_id} - {task_name} - {label}")
                continue

            # Create figure
            plt.figure()
            plt.scatter(x_vals, y_vals, label=label, marker='o', color='blue')

            # Draw rectangle boxes if Width and Height are present
            for entry in entries:
                if all(k in entry for k in ("X", "Y", "Width", "Height")):
                    x = entry["X"]
                    y = entry["Y"]
                    w = entry["Width"]
                    h = entry["Height"]
                    if isinstance(x, (int, float)) and isinstance(y, (int, float)) and \
                       isinstance(w, (int, float)) and isinstance(h, (int, float)):
                        rect = patches.Rectangle((x, y), w, h, linewidth=1, edgecolor='red', facecolor='none')
                        plt.gca().add_patch(rect)

            plt.title(f"{subject_id} - {task_name} - {label}")
            plt.xlabel("X")
            plt.ylabel("Y")
            # Invert y-Axis
            plt.gca().invert_yaxis()
            # plt.legend()

            # Save the plot
            safe_subject = sanitize_filename(subject_id)
            safe_task = sanitize_filename(task_name)
            safe_label = sanitize_filename(label)

            # Create new filename
            filename = path + f"plots/{safe_subject}_{safe_task}_{safe_label}.png"

            # Save and close file
            plt.savefig(filename)
            plt.close()
            print(f"  Plot saved: {filename}")

print("Plotting completed.")
