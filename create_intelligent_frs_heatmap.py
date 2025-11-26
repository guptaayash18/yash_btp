import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.colors import LinearSegmentedColormap
import os

# Change to the correct directory
os.chdir(r'C:\Users\Abhijit\OneDrive - iitkgp.ac.in\Desktop\Gupta_BTP')

print("=" * 80)
print("INTELLIGENT FRS ANALYSIS - MAXIMUM FIRE RISK BY LOCATION")
print("=" * 80)

# Read the CSV
df = pd.read_csv('Untitled spreadsheet - opencast_15points_12flights_dataset.csv')

print(f"\nTotal data: {len(df):,} rows")
print(f"Date range: {df['timestamp'].min()} to {df['timestamp'].max()}")

# Filter for FL01 only for consistency
df_fl01 = df[df['flight_id'] == 'FL01'].copy()
print(f"FL01 data: {len(df_fl01):,} rows")

# Analyze fire risk for each point over the ENTIRE YEAR
print("\n" + "=" * 80)
print("ANALYZING FIRE RISK PATTERNS OVER ENTIRE YEAR")
print("=" * 80)

point_analysis = []

for point_id in range(1, 16):
    point_data = df_fl01[df_fl01['point_id'] == point_id]['FRS']
    
    # Calculate various metrics
    max_frs = point_data.max()
    mean_frs = point_data.mean()
    p95_frs = point_data.quantile(0.95)  # 95th percentile
    p99_frs = point_data.quantile(0.99)  # 99th percentile
    
    # Count high-risk events
    count_20plus = (point_data >= 20).sum()
    count_40plus = (point_data >= 40).sum()
    count_60plus = (point_data >= 60).sum()
    
    point_analysis.append({
        'point_id': point_id,
        'max_frs': max_frs,
        'p99_frs': p99_frs,
        'p95_frs': p95_frs,
        'mean_frs': mean_frs,
        'events_20plus': count_20plus,
        'events_40plus': count_40plus,
        'events_60plus': count_60plus
    })

point_summary = pd.DataFrame(point_analysis)

print("\nFire Risk Summary by Point:")
print(point_summary.to_string(index=False))

# Create 5x3 grid with MAXIMUM FRS values
grid_max = np.zeros((3, 5))
grid_p95 = np.zeros((3, 5))
grid_events = np.zeros((3, 5))

for _, row in point_summary.iterrows():
    point = int(row['point_id'])
    row_idx = (point - 1) // 5
    col_idx = (point - 1) % 5
    
    grid_max[row_idx, col_idx] = row['max_frs']
    grid_p95[row_idx, col_idx] = row['p95_frs']
    grid_events[row_idx, col_idx] = row['events_20plus']

print("\nMaximum FRS Grid (Worst-case at each point):")
print(grid_max)

# Color scheme
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
cmap = LinearSegmentedColormap.from_list('frs_smart', list(zip(positions, color_values)), N=n_bins)

# ============================================================================
# HEATMAP 1: Maximum FRS (Worst-case scenario)
# ============================================================================
fig, ax = plt.subplots(figsize=(18, 10))
fig.patch.set_facecolor('white')

im = ax.imshow(grid_max, cmap=cmap, vmin=0, vmax=80, aspect='auto', 
               interpolation='gaussian', alpha=1.0)

ax.set_xticks([])
ax.set_yticks([])
ax.tick_params(length=0)

# Gridlines
for i in range(4):
    ax.axvline(i + 0.5, color='white', linewidth=4, alpha=1.0)
for i in range(2):
    ax.axhline(i + 0.5, color='white', linewidth=4, alpha=1.0)

# Annotations
for i in range(3):
    for j in range(5):
        point_id = i * 5 + j + 1
        frs_value = grid_max[i, j]
        
        text_color = 'white' if frs_value > 40 else 'black'
        
        # Point number
        ax.text(j, i - 0.28, f'Point {point_id}',
                ha='center', va='center', fontsize=14, fontweight='bold',
                color=text_color)
        
        # Max FRS value
        ax.text(j, i + 0.08, f'{frs_value:.2f}',
                ha='center', va='center', fontsize=38, fontweight='bold',
                color=text_color)
        
        # High-risk event count
        events = int(grid_events[i, j])
        if events > 0:
            ax.text(j, i + 0.35, f'{events} events',
                    ha='center', va='center', fontsize=11, 
                    color=text_color, style='italic')

plt.suptitle('Maximum Fire Risk Score by Location (FL01 - Full Year)',
             fontsize=24, fontweight='bold', y=0.96)
ax.set_title('Shows worst-case FRS at each monitoring point | Nov 2024 - Nov 2025',
             fontsize=13, pad=15)

cbar = plt.colorbar(im, ax=ax, orientation='vertical', pad=0.02, fraction=0.04)
cbar.set_label('Fire Risk Score (Maximum)', fontsize=14, fontweight='bold', 
               rotation=270, labelpad=25)
cbar.ax.tick_params(labelsize=11)

# Risk threshold lines
cbar.ax.axhline(20, color='white', linewidth=2, linestyle='--', alpha=0.8)
cbar.ax.axhline(40, color='white', linewidth=2, linestyle='--', alpha=0.8)
cbar.ax.axhline(60, color='white', linewidth=2, linestyle='--', alpha=0.8)

legend_elements = [
    mpatches.Patch(facecolor='#00e400', edgecolor='black', linewidth=1.5, 
                   label='Safe (< 20)'),
    mpatches.Patch(facecolor='#ffff00', edgecolor='black', linewidth=1.5, 
                   label='Monitor (20-60)'),
    mpatches.Patch(facecolor='#ff0000', edgecolor='black', linewidth=1.5, 
                   label='High Risk (≥ 60)')
]

ax.legend(handles=legend_elements, loc='upper center', bbox_to_anchor=(0.5, -0.05),
          ncol=3, fontsize=13, frameon=True, shadow=False)

plt.tight_layout()

output1 = 'FL01_FRS_Maximum_Risk_Heatmap.png'
plt.savefig(output1, dpi=300, bbox_inches='tight', facecolor='white')
print(f"\nMaximum FRS heatmap saved as: {output1}")
plt.close()

# ============================================================================
# HEATMAP 2: 95th Percentile (High-risk threshold)
# ============================================================================
fig, ax = plt.subplots(figsize=(18, 10))
fig.patch.set_facecolor('white')

im = ax.imshow(grid_p95, cmap=cmap, vmin=0, vmax=80, aspect='auto', 
               interpolation='gaussian', alpha=1.0)

ax.set_xticks([])
ax.set_yticks([])
ax.tick_params(length=0)

for i in range(4):
    ax.axvline(i + 0.5, color='white', linewidth=4, alpha=1.0)
for i in range(2):
    ax.axhline(i + 0.5, color='white', linewidth=4, alpha=1.0)

for i in range(3):
    for j in range(5):
        point_id = i * 5 + j + 1
        frs_value = grid_p95[i, j]
        
        text_color = 'white' if frs_value > 40 else 'black'
        
        ax.text(j, i - 0.25, f'Point {point_id}',
                ha='center', va='center', fontsize=14, fontweight='bold',
                color=text_color)
        
        ax.text(j, i + 0.15, f'{frs_value:.2f}',
                ha='center', va='center', fontsize=38, fontweight='bold',
                color=text_color)

plt.suptitle('95th Percentile Fire Risk Score by Location',
             fontsize=24, fontweight='bold', y=0.96)
ax.set_title('Shows typical high-risk conditions (top 5% of readings) | FL01 Full Year',
             fontsize=13, pad=15)

cbar = plt.colorbar(im, ax=ax, orientation='vertical', pad=0.02, fraction=0.04)
cbar.set_label('FRS (95th Percentile)', fontsize=14, fontweight='bold', 
               rotation=270, labelpad=25)
cbar.ax.tick_params(labelsize=11)
cbar.ax.axhline(20, color='white', linewidth=2, linestyle='--', alpha=0.8)
cbar.ax.axhline(40, color='white', linewidth=2, linestyle='--', alpha=0.8)
cbar.ax.axhline(60, color='white', linewidth=2, linestyle='--', alpha=0.8)

ax.legend(handles=legend_elements, loc='upper center', bbox_to_anchor=(0.5, -0.05),
          ncol=3, fontsize=13, frameon=True, shadow=False)

plt.tight_layout()

output2 = 'FL01_FRS_P95_Heatmap.png'
plt.savefig(output2, dpi=300, bbox_inches='tight', facecolor='white')
print(f"95th percentile heatmap saved as: {output2}")
plt.close()

# ============================================================================
# ANALYSIS SUMMARY
# ============================================================================
print("\n" + "=" * 80)
print("FIRE RISK ANALYSIS SUMMARY")
print("=" * 80)

print(f"\nHighest Risk Location:")
max_point = point_summary.loc[point_summary['max_frs'].idxmax()]
print(f"  Point {int(max_point['point_id'])}: Max FRS = {max_point['max_frs']:.2f}")
print(f"  - Had {int(max_point['events_20plus'])} instances where FRS ≥ 20")
print(f"  - Had {int(max_point['events_40plus'])} instances where FRS ≥ 40")
if max_point['events_60plus'] > 0:
    print(f"  - Had {int(max_point['events_60plus'])} instances where FRS ≥ 60 (SERIOUS)")

print(f"\nSafest Location:")
min_point = point_summary.loc[point_summary['max_frs'].idxmin()]
print(f"  Point {int(min_point['point_id'])}: Max FRS = {min_point['max_frs']:.2f}")

# Overall statistics
total_high_risk = point_summary['events_20plus'].sum()
total_critical = point_summary['events_40plus'].sum()
total_serious = point_summary['events_60plus'].sum()

print(f"\nOverall Fire Risk Events (FL01, Full Year):")
print(f"  Total measurements: {len(df_fl01):,}")
print(f"  Events with FRS ≥ 20: {int(total_high_risk):,} ({total_high_risk/len(df_fl01)*100:.2f}%)")
print(f"  Events with FRS ≥ 40: {int(total_critical):,} ({total_critical/len(df_fl01)*100:.2f}%)")
print(f"  Events with FRS ≥ 60: {int(total_serious):,} ({total_serious/len(df_fl01)*100:.2f}%)")

# Find specific high-risk events
print(f"\nTop 5 Highest FRS Events:")
top_events = df_fl01.nlargest(5, 'FRS')[['timestamp', 'point_id', 'FRS', 'GR', 'CO_ppm', 'CH4_ppm', 'Temperature (°C)', 'O2_percentage']]
print(top_events.to_string(index=False))

print("\n" + "=" * 80)
print("INTELLIGENT FRS HEATMAPS CREATED!")
print("=" * 80)
print("\nTwo heatmaps created:")
print("  1. Maximum FRS - Shows worst-case fire risk at each location")
print("  2. 95th Percentile - Shows typical high-risk conditions")
print("\nThese show WHERE fire risks actually occurred over the year!")
print("=" * 80)

