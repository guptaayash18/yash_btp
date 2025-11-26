import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.patheffects as path_effects
from matplotlib.colors import LinearSegmentedColormap
import os

# Change to the correct directory
os.chdir(r'C:\Users\Abhijit\OneDrive - iitkgp.ac.in\Desktop\Gupta_BTP')

print("=" * 80)
print("CREATING BEAUTIFUL GRADIENT HEATMAP - FL01 SNAPSHOT")
print("=" * 80)

# Read the CSV
df = pd.read_csv('Untitled spreadsheet - opencast_15points_12flights_dataset.csv')

# Filter for FL01 and first timestamp (06:00:00)
df_fl01 = df[(df['flight_id'] == 'FL01') & (df['timestamp'].str.contains('06:00:00'))].copy()

# Take the first occurrence
timestamp = df_fl01['timestamp'].iloc[0]
df_snapshot = df_fl01[df_fl01['timestamp'] == timestamp].copy()

print(f"\nUsing snapshot: {timestamp}")
print(f"Data points: {len(df_snapshot)} (15 monitoring points)")

# For each point, get the dominant pollutant and its AQI
point_data = []

for _, row in df_snapshot.iterrows():
    point_id = int(row['point_id'])
    dominant_pollutant = row['Dominant_Pollutant']
    
    # Get the corresponding AQI value
    aqi_col = f"{dominant_pollutant}_AQI"
    aqi_value = row[aqi_col]
    
    point_data.append({
        'point_id': point_id,
        'dominant_pollutant': dominant_pollutant,
        'aqi': aqi_value
    })

# Create DataFrame and sort by point_id
point_summary = pd.DataFrame(point_data).sort_values('point_id')

print("\nPoint Summary:")
print(point_summary.to_string(index=False))

# Arrange in 5x3 grid
grid = np.zeros((3, 5))
pollutant_grid = [['' for _ in range(5)] for _ in range(3)]

for _, row in point_summary.iterrows():
    point = int(row['point_id'])
    aqi = row['aqi']
    pollutant = row['dominant_pollutant']
    
    row_idx = (point - 1) // 5
    col_idx = (point - 1) % 5
    
    grid[row_idx, col_idx] = aqi
    pollutant_grid[row_idx][col_idx] = pollutant

# EXACT COLORS FROM AQI TABLE - SMOOTHER TRANSITIONS
colors = [
    (0.0, '#00e400'),      # Bright Green (0)
    (0.05, '#4dff00'),     # Transition
    (0.10, '#7dff00'),     # Light Green (50)
    (0.15, '#a6f600'),     # Yellow-Green
    (0.20, '#d4ff00'),     # Lime Yellow (100)
    (0.25, '#f7ff00'),     # Yellow
    (0.30, '#ffee00'),     # Golden Yellow
    (0.35, '#ffdd00'),     # Gold
    (0.40, '#ffcc00'),     # Deep Gold (200)
    (0.45, '#ffaa00'),     # Light Orange
    (0.50, '#ff9900'),     # Orange
    (0.55, '#ff7700'),     # Deep Orange
    (0.60, '#ff5500'),     # Red-Orange (300)
    (0.65, '#ff3300'),     # Red
    (0.70, '#ff0000'),     # Pure Red
    (0.75, '#ee0000'),     # Deep Red
    (0.80, '#cc0000'),     # Darker Red (400)
    (0.85, '#aa0000'),     # Very Dark Red
    (0.90, '#880000'),     # Maroon
    (1.0, '#660000')       # Dark Maroon (500)
]

# Create super smooth colormap
n_bins = 1000  # Even smoother!
positions = [pos for pos, _ in colors]
color_values = [color for _, color in colors]
cmap = LinearSegmentedColormap.from_list('aqi_smooth', list(zip(positions, color_values)), N=n_bins)

# Create figure
fig, ax = plt.subplots(figsize=(20, 12))
fig.patch.set_facecolor('#f8f8f8')

# Plot heatmap with maximum smoothness
im = ax.imshow(grid, cmap=cmap, vmin=0, vmax=500, aspect='auto', 
               interpolation='gaussian', alpha=0.98)

# Set ticks
ax.set_xticks(np.arange(5))
ax.set_yticks(np.arange(3))
ax.set_xticklabels([])
ax.set_yticklabels([])
ax.tick_params(which='both', length=0)

# Add beautiful gridlines
for i in range(4):
    ax.axvline(i + 0.5, color='white', linewidth=5, alpha=0.9)
for i in range(2):
    ax.axhline(i + 0.5, color='white', linewidth=5, alpha=0.9)

# Annotate cells with beautiful styling
for i in range(3):
    for j in range(5):
        point_id = i * 5 + j + 1
        aqi_value = grid[i, j]
        pollutant = pollutant_grid[i][j]
        
        # Smart text color based on background
        if aqi_value < 50:
            text_color = 'black'
        elif aqi_value < 200:
            text_color = 'black'
        else:
            text_color = 'white'
        
        # Point ID with elegant styling
        ax.text(j, i - 0.30, f'Point {point_id}',
                ha='center', va='center', fontsize=16, fontweight='bold',
                color=text_color,
                bbox=dict(boxstyle='round,pad=0.5', 
                         facecolor=(0, 0, 0, 0.7) if text_color == 'white' else (1, 1, 1, 0.8),
                         edgecolor='none'))
        
        # AQI value - LARGE and prominent
        ax.text(j, i + 0.05, f'{aqi_value:.1f}',
                ha='center', va='center', fontsize=38, fontweight='bold',
                color=text_color,
                path_effects=[path_effects.withStroke(linewidth=4, 
                             foreground='black' if text_color == 'white' else 'white', alpha=0.4)])
        
        # Pollutant name with style
        ax.text(j, i + 0.35, pollutant,
                ha='center', va='center', fontsize=14, fontstyle='italic',
                fontweight='600', color=text_color,
                bbox=dict(boxstyle='round,pad=0.35', 
                         facecolor=(0, 0, 0, 0.6) if text_color == 'white' else (1, 1, 1, 0.7),
                         edgecolor='none'))

# Beautiful title
plt.suptitle('Opencast Mining Site - Air Quality Index Snapshot',
             fontsize=26, fontweight='bold', y=0.98, color='#2c3e50')
ax.set_title(f'Flight FL01 | AQI by Dominant Pollutant | {timestamp}',
             fontsize=16, pad=25, style='italic', color='#34495e')

# Colorbar with exact categories
cbar = plt.colorbar(im, ax=ax, orientation='vertical', pad=0.02, fraction=0.046)
cbar.set_label('Air Quality Index (AQI)', fontsize=16, fontweight='bold', 
               rotation=270, labelpad=35)
cbar.ax.tick_params(labelsize=13)

# Add category lines and labels on colorbar
aqi_categories = [
    (25, 'Good\n0-50', '#00e400'),
    (75, 'Satisfactory\n51-100', '#7dff00'),
    (150, 'Moderately\nPolluted\n101-200', '#ffcc00'),
    (250, 'Poor\n201-300', '#ff9900'),
    (350, 'Very Poor\n301-400', '#ff0000'),
    (450, 'Severe\n401-500', '#880000')
]

for aqi_val, label, color in aqi_categories:
    cbar.ax.text(2.5, aqi_val, label, va='center', ha='center', 
                fontsize=11, fontweight='bold',
                bbox=dict(boxstyle='round,pad=0.5', facecolor='white', 
                         edgecolor='gray', alpha=0.95, linewidth=1.5))

# Legend at bottom with EXACT colors
legend_elements = [
    mpatches.Patch(facecolor='#00e400', edgecolor='black', linewidth=2, label='Good (0-50)'),
    mpatches.Patch(facecolor='#7dff00', edgecolor='black', linewidth=2, label='Satisfactory (51-100)'),
    mpatches.Patch(facecolor='#ffcc00', edgecolor='black', linewidth=2, label='Moderately Polluted (101-200)'),
    mpatches.Patch(facecolor='#ff9900', edgecolor='black', linewidth=2, label='Poor (201-300)'),
    mpatches.Patch(facecolor='#ff0000', edgecolor='black', linewidth=2, label='Very Poor (301-400)'),
    mpatches.Patch(facecolor='#880000', edgecolor='white', linewidth=2, label='Severe (401-500)')
]

legend = ax.legend(handles=legend_elements, loc='upper left', bbox_to_anchor=(-0.01, -0.08),
                   ncol=6, fontsize=13, frameon=True, fancybox=True, shadow=True,
                   title='AQI Categories', title_fontsize=14)
legend.get_frame().set_facecolor('white')
legend.get_frame().set_alpha(0.95)
legend.get_frame().set_linewidth(2)

# Info text
info_text = f"Snapshot: {timestamp} | 15 Monitoring Points | Smooth Gradient Visualization"
fig.text(0.5, 0.015, info_text, ha='center', fontsize=12, 
         style='italic', color='#555555', weight='600')

plt.tight_layout()

# Save high-quality outputs
output_file = 'FL01_Beautiful_Gradient_Heatmap.png'
plt.savefig(output_file, dpi=400, bbox_inches='tight', facecolor='#f8f8f8')
print(f"\nBeautiful heatmap saved as: {output_file}")

output_pdf = 'FL01_Beautiful_Gradient_Heatmap.pdf'
plt.savefig(output_pdf, format='pdf', bbox_inches='tight', facecolor='#f8f8f8')
print(f"PDF version saved as: {output_pdf}")

plt.show()

print("\n" + "=" * 80)
print("STUNNING GRADIENT HEATMAP CREATED!")
print("=" * 80)

print("\nSnapshot Summary:")
print(f"  Highest AQI: Point {point_summary.loc[point_summary['aqi'].idxmax(), 'point_id']} "
      f"({point_summary['aqi'].max():.1f}) - {point_summary.loc[point_summary['aqi'].idxmax(), 'dominant_pollutant']}")
print(f"  Lowest AQI:  Point {point_summary.loc[point_summary['aqi'].idxmin(), 'point_id']} "
      f"({point_summary['aqi'].min():.1f}) - {point_summary.loc[point_summary['aqi'].idxmin(), 'dominant_pollutant']}")

print("\nDominant Pollutants:")
pollutant_counts = point_summary['dominant_pollutant'].value_counts()
for pollutant, count in pollutant_counts.items():
    print(f"  {pollutant}: {count} point(s)")

print("\nColor scheme: Smooth gradients from GREEN -> YELLOW -> ORANGE -> RED -> DARK RED")
print("=" * 80)

