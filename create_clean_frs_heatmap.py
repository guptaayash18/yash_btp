import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.colors import LinearSegmentedColormap
import os

# Change to the correct directory
os.chdir(r'C:\Users\Abhijit\OneDrive - iitkgp.ac.in\Desktop\Gupta_BTP')

print("=" * 80)
print("CREATING CLEAN FRS HEATMAP - FL01")
print("=" * 80)

# Read the CSV
df = pd.read_csv('Untitled spreadsheet - opencast_15points_12flights_dataset.csv')

# Filter for FL01 and first timestamp
df_fl01 = df[(df['flight_id'] == 'FL01') & (df['timestamp'].str.contains('06:00:00'))].copy()
timestamp = df_fl01['timestamp'].iloc[0]
df_snapshot = df_fl01[df_fl01['timestamp'] == timestamp].copy()

print(f"\nUsing snapshot: {timestamp}")

# Extract FRS values
point_data = []
for _, row in df_snapshot.iterrows():
    point_data.append({
        'point_id': int(row['point_id']),
        'frs': row['FRS']
    })

point_summary = pd.DataFrame(point_data).sort_values('point_id')

# Create 5x3 grid
grid = np.zeros((3, 5))
for _, row in point_summary.iterrows():
    point = int(row['point_id'])
    frs = row['frs']
    row_idx = (point - 1) // 5
    col_idx = (point - 1) % 5
    grid[row_idx, col_idx] = frs

# Simple color scheme - Green to Red
colors = [
    (0.0, '#00e400'),    # Green (0)
    (0.25, '#92d050'),   # Light green (20)
    (0.50, '#ffff00'),   # Yellow (40)
    (0.75, '#ff9900'),   # Orange (60)
    (1.0, '#ff0000')     # Red (80)
]

n_bins = 1000
positions = [pos for pos, _ in colors]
color_values = [color for _, color in colors]
cmap = LinearSegmentedColormap.from_list('frs_clean', list(zip(positions, color_values)), N=n_bins)

# Create figure - CLEAN AND SIMPLE
fig, ax = plt.subplots(figsize=(18, 10))
fig.patch.set_facecolor('white')

# Plot heatmap
im = ax.imshow(grid, cmap=cmap, vmin=0, vmax=80, aspect='auto', 
               interpolation='gaussian', alpha=1.0)

# Remove ticks
ax.set_xticks([])
ax.set_yticks([])
ax.tick_params(length=0)

# Clean white gridlines
for i in range(4):
    ax.axvline(i + 0.5, color='white', linewidth=4, alpha=1.0)
for i in range(2):
    ax.axhline(i + 0.5, color='white', linewidth=4, alpha=1.0)

# Simple annotations - just point number and FRS value
for i in range(3):
    for j in range(5):
        point_id = i * 5 + j + 1
        frs_value = grid[i, j]
        
        # Smart text color
        text_color = 'white' if frs_value > 40 else 'black'
        
        # Point number (smaller, top)
        ax.text(j, i - 0.25, f'Point {point_id}',
                ha='center', va='center', fontsize=14, fontweight='bold',
                color=text_color)
        
        # FRS value (large, center)
        ax.text(j, i + 0.15, f'{frs_value:.2f}',
                ha='center', va='center', fontsize=42, fontweight='bold',
                color=text_color)

# Simple title
plt.suptitle('Fire Risk Score - Monitoring Points',
             fontsize=24, fontweight='bold', y=0.96)
ax.set_title(f'Flight FL01 | {timestamp}',
             fontsize=14, pad=15)

# Clean colorbar
cbar = plt.colorbar(im, ax=ax, orientation='vertical', pad=0.02, fraction=0.04)
cbar.set_label('Fire Risk Score', fontsize=14, fontweight='bold', rotation=270, labelpad=25)
cbar.ax.tick_params(labelsize=11)

# Simple risk markers on colorbar
cbar.ax.axhline(20, color='white', linewidth=2, linestyle='--')
cbar.ax.axhline(40, color='white', linewidth=2, linestyle='--')
cbar.ax.axhline(60, color='white', linewidth=2, linestyle='--')

# Simple legend - only 3 key categories
legend_elements = [
    mpatches.Patch(facecolor='#00e400', edgecolor='black', linewidth=1.5, 
                   label='Safe (< 20)'),
    mpatches.Patch(facecolor='#ffff00', edgecolor='black', linewidth=1.5, 
                   label='Monitor (20-60)'),
    mpatches.Patch(facecolor='#ff0000', edgecolor='black', linewidth=1.5, 
                   label='Emergency (≥ 60)')
]

ax.legend(handles=legend_elements, loc='upper center', bbox_to_anchor=(0.5, -0.05),
          ncol=3, fontsize=13, frameon=True, shadow=False)

plt.tight_layout()

# Save
output_file = 'FL01_FRS_Clean_Heatmap.png'
plt.savefig(output_file, dpi=300, bbox_inches='tight', facecolor='white')
print(f"\nClean heatmap saved as: {output_file}")

output_pdf = 'FL01_FRS_Clean_Heatmap.pdf'
plt.savefig(output_pdf, format='pdf', bbox_inches='tight', facecolor='white')
print(f"PDF saved as: {output_pdf}")

plt.show()

print("\n" + "=" * 80)
print("CLEAN FRS HEATMAP CREATED!")
print("=" * 80)
print(f"Highest: Point {point_summary.loc[point_summary['frs'].idxmax(), 'point_id']} ({point_summary['frs'].max():.2f})")
print(f"Lowest:  Point {point_summary.loc[point_summary['frs'].idxmin(), 'point_id']} ({point_summary['frs'].min():.2f})")
print("=" * 80)

