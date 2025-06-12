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

# Plott dimensions

plottSize = 1400
plottStart = 0

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
        
        if len(labels.items()) < 3:
            continue

        for label, entries in labels.items():           
            x_vals = [e["X"] for e in entries if "X" in e]
            y_vals = [e["Y"] for e in entries if "Y" in e]

            # Skip plots with no coordinates
            if not x_vals or not y_vals:
                print(f"  Skipping empty plot: {subject_id} - {task_name}")
                continue

        # Create figure
        plt.figure()
        plt.title(f"{subject_id} - {task_name}")

        for label, entries in labels.items():

            x_vals = [e["X"] for e in entries if "X" in e]
            y_vals = [e["Y"] for e in entries if "Y" in e]

            color = 'blue'
            
            if ":one:" in label: 
                color = "red"
            if ":two:" in label:
                color = "green"
            if "three" in label:
                color = "blue"


            # Draw rectangle boxes if Width and Height are present
            for entry in entries:
                if all(k in entry for k in ("X", "Y", "Width", "Height")):
                    x = entry["X"]
                    y = entry["Y"]
                    w = entry["Width"]
                    h = entry["Height"]
                    if isinstance(x, (int, float)) and isinstance(y, (int, float)) and \
                       isinstance(w, (int, float)) and isinstance(h, (int, float)):
                        rect = patches.Rectangle((x, y), w, h, linewidth=1, edgecolor=color, facecolor='none')
                        plt.gca().add_patch(rect)

            plt.scatter(x_vals, y_vals, label=label, marker='o', color=color)

            plt.xlabel("X")
            plt.ylabel("Y")
            plt.xlim(plottStart, plottSize)
            plt.ylim(plottStart, plottSize)
            # Invert y-Axis
            plt.gca().invert_yaxis()
            plt.legend()

        # Grid lines to divide plot into 9 parts (3x3 grid)
        for i in range(1, 3):
            plt.axhline(i * plottSize / 3, color='lightgray', linestyle='--', linewidth=0.5)
            plt.axvline(i * plottSize / 3, color='lightgray', linestyle='--', linewidth=0.5)

        plt.grid(True, which='both', linestyle=':', linewidth=0.3)

        # Save the plot
        safe_subject = sanitize_filename(subject_id)
        safe_task = sanitize_filename(task_name)
        #safe_label = sanitize_filename(label)

        # Create new filename
        filename = path + f"plots/{safe_subject}_{safe_task}.png"

        # Save and close file
        plt.savefig(filename)
        plt.close()
        print(f"  Plot saved: {filename}")

print("Plotting completed.")
