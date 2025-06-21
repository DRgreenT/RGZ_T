import json
import os
import re
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.image as mpimg
import gc
from pathlib import Path

# Makes sure filenames don't contain illegal characters for Windows
def sanitize_filename(s):
    s = s.replace('\n', ' ').strip()
    s = re.sub(r'[<>:"/\\|?*]', '_', s)
    s = re.sub(r'\s+', '_', s)
    return s

# Plott dimensions
plottSizeY = 1000
plottSizeX = 1000
plottStart = 0

# Json file path
path = "C:\\Users\\thoma\\source\\repos\\_projects\\RGZ_T\\bin\\Debug\\net9.0\\"

# Background image path as Path object
imagesPath = Path(path) / "images"

# Get all image paths
allImagesPaths = list(imagesPath.glob("*.png"))

# Ensure output directory exists
os.makedirs(path + "plots", exist_ok=True)

# Load the JSON data
json_path = path + "subjects_output.json"
print(f"Loading data from {json_path}...")
with open(json_path, "r", encoding="utf-8") as f:
    data = json.load(f)

print(f"Loaded {len(data)} subjects.")

debugCounter = 0
imagesNotFoundCounter = 0
skippedNoCoordinates = 0

# Iterate over all subjects and tasks
for subject_index, (subject_id, subject) in enumerate(data.items(), start=1):
    

    #if debugCounter >= 50:
    #   break
    tasks = subject.get("Tasks", {})
    subjectName = subject.get("subject ID")

    print(f"[{subject_index}/{len(data)}] Processing subject {subject_id} with {len(tasks)} tasks...")

    for task_name, labels in tasks.items():
        
        # Skip if less than a certain amout of "tasks" are found
        if len(labels.items()) < 3:
            continue

        # Skip plots with no coordinates
        for label, entries in labels.items():
            x_vals = [e["X"] for e in entries if "X" in e]
            y_vals = [e["Y"] for e in entries if "Y" in e]

            if not x_vals or not y_vals:
                print(f"  Skipping empty plot: {subject_id} - {task_name}")
                skippedNoCoordinates += 1
                continue

        # Default: no background / try to finde image that contains "subject name"
        fig, ax = plt.subplots(figsize=(10, 10), dpi=100)
        bg_found = False

        for image in allImagesPaths:
            if subjectName in image.name:
                bg_img = mpimg.imread(image)
                x0 = 0
                y0 = 0
                img_width = 1020
                img_height = 1020
                ax.imshow(bg_img, extent=(x0, x0 + img_width, y0 + img_height, y0), zorder=0)
                bg_found = True
                break

        # Skip if no image was found
        if bg_found is False:
            imagesNotFoundCounter += 1
            plt.close(fig)
            continue
        
        # Set plot title
        plt.title(f"{subject_id} - {task_name}")

        # Get coordinates
        for label, entries in labels.items():
            x_vals = [e["X"] for e in entries if "X" in e]
            y_vals = [e["Y"] for e in entries if "Y" in e]

            # Set colors for the plot markers
            color = 'blue'
            if ":one:" in label:
                color = "blue"
            if ":two:" in label:
                color = "green"
            if "three" in label:
                color = "purple"

            # Try and draw squares if entries contain "width and hight"
            for entry in entries:
                if all(k in entry for k in ("X", "Y", "Width", "Height")):
                    x = entry["X"]
                    y = entry["Y"]
                    w = entry["Width"]
                    h = entry["Height"]
                    if isinstance(x, (int, float)) and isinstance(y, (int, float)) and \
                       isinstance(w, (int, float)) and isinstance(h, (int, float)):
                        rect = patches.Rectangle((x, y), w, h, linewidth=1, edgecolor=color, facecolor='none')
                        ax.add_patch(rect)

            # Set markers colors and shapes for the labels 
            if color is "green":
                ax.scatter(x_vals, y_vals, label=label, marker='o', facecolors='none', edgecolors=color, s=100)
            else:
                ax.scatter(x_vals, y_vals, label=label, marker='o', color=color, s=10)

            # Axis labels and limits
            ax.set_xlabel("X")
            ax.set_ylabel("Y")
            ax.set_xlim(plottStart, plottSizeX)
            ax.set_ylim(plottStart, plottSizeY)

            # Invert y-axis
            ax.invert_yaxis()

            # Set legend
            ax.legend(loc='lower center', bbox_to_anchor=(0.5, -0.1), ncol=2, fontsize='small')

        # Create file name for new image
        safe_subject = sanitize_filename(subjectName)
        safe_task = sanitize_filename(task_name)
        filename = path + f"plots/{safe_subject}.png"

        # Save and close new image
        plt.savefig(filename)
        plt.close()
        print(f"  Plot saved: {filename}")
        debugCounter += 1
        gc.collect()

# Final info
print("Plotting completed.")
print(f"Plots skipped (no images): {imagesNotFoundCounter}")
print(f"Plots skipped (no coordinates): {skippedNoCoordinates}")
