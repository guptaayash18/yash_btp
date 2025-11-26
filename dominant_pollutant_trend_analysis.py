import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import os

# Change to the correct directory
os.chdir(r'C:\Users\Abhijit\OneDrive - iitkgp.ac.in\Desktop\Gupta_BTP')

print("=" * 80)
print("COMPREHENSIVE TREND ANALYSIS - DOMINANT POLLUTANT")
print("=" * 80)

# Read the CSV
df = pd.read_csv('Untitled spreadsheet - opencast_15points_12flights_dataset.csv')

print(f"\nTotal data: {len(df):,} rows")
print(f"Date range: {df['timestamp'].min()} to {df['timestamp'].max()}")

# Convert timestamp to datetime
df['timestamp'] = pd.to_datetime(df['timestamp'])
df['date'] = df['timestamp'].dt.date
df['month'] = df['timestamp'].dt.month
df['month_name'] = df['timestamp'].dt.strftime('%b')
df['hour'] = df['timestamp'].dt.hour
df['day_of_week'] = df['timestamp'].dt.day_name()
df['week'] = df['timestamp'].dt.isocalendar().week

print("\nData prepared for analysis")

# Create output directory for plots
output_dir = 'Dominant_Pollutant_Analysis'
if not os.path.exists(output_dir):
    os.makedirs(output_dir)
    print(f"Created directory: {output_dir}")

# Set style
sns.set_style("whitegrid")
plt.rcParams['figure.facecolor'] = 'white'

# ============================================================================
# ANALYSIS 1: Overall Distribution of Dominant Pollutants
# ============================================================================
print("\n" + "=" * 80)
print("ANALYSIS 1: Overall Distribution")
print("=" * 80)

pollutant_counts = df['Dominant_Pollutant'].value_counts()
pollutant_pct = (pollutant_counts / len(df) * 100).round(2)

print("\nDominant Pollutant Distribution:")
for pollutant, count in pollutant_counts.items():
    pct = pollutant_pct[pollutant]
    print(f"  {pollutant:8s}: {count:8,} ({pct:6.2f}%)")

# Plot
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))

# Bar chart
colors = {'NOx': '#e74c3c', 'CO': '#f39c12', 'PM10': '#3498db', 'PM2.5': '#9b59b6', 'SO2': '#1abc9c'}
bars = ax1.bar(pollutant_counts.index, pollutant_counts.values, 
               color=[colors.get(p, '#95a5a6') for p in pollutant_counts.index],
               edgecolor='black', linewidth=1.5)
ax1.set_xlabel('Pollutant', fontsize=14, fontweight='bold')
ax1.set_ylabel('Frequency', fontsize=14, fontweight='bold')
ax1.set_title('Overall Distribution of Dominant Pollutants', fontsize=16, fontweight='bold')
ax1.tick_params(labelsize=12)
for bar in bars:
    height = bar.get_height()
    ax1.text(bar.get_x() + bar.get_width()/2., height,
            f'{int(height):,}\n({height/len(df)*100:.1f}%)',
            ha='center', va='bottom', fontsize=11, fontweight='bold')

# Pie chart
ax2.pie(pollutant_counts.values, labels=pollutant_counts.index, autopct='%1.1f%%',
        colors=[colors.get(p, '#95a5a6') for p in pollutant_counts.index],
        startangle=90, textprops={'fontsize': 12, 'fontweight': 'bold'},
        wedgeprops={'edgecolor': 'black', 'linewidth': 1.5})
ax2.set_title('Percentage Distribution', fontsize=16, fontweight='bold')

plt.tight_layout()
plt.savefig(f'{output_dir}/01_overall_distribution.png', dpi=300, bbox_inches='tight')
print(f"Saved: 01_overall_distribution.png")
plt.close()

# ============================================================================
# ANALYSIS 2: Monthly Trends
# ============================================================================
print("\n" + "=" * 80)
print("ANALYSIS 2: Monthly Trends")
print("=" * 80)

monthly_pollutants = df.groupby(['month_name', 'Dominant_Pollutant']).size().unstack(fill_value=0)
month_order = ['Nov', 'Dec', 'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct']
monthly_pollutants = monthly_pollutants.reindex([m for m in month_order if m in monthly_pollutants.index])

print("\nMonthly Distribution:")
print(monthly_pollutants)

# Stacked bar chart
fig, ax = plt.subplots(figsize=(18, 8))
monthly_pollutants.plot(kind='bar', stacked=True, ax=ax, 
                        color=[colors.get(p, '#95a5a6') for p in monthly_pollutants.columns],
                        edgecolor='black', linewidth=0.5)
ax.set_xlabel('Month', fontsize=14, fontweight='bold')
ax.set_ylabel('Frequency', fontsize=14, fontweight='bold')
ax.set_title('Monthly Trend of Dominant Pollutants (Stacked)', fontsize=16, fontweight='bold')
ax.legend(title='Pollutant', title_fontsize=13, fontsize=12, loc='upper right')
ax.tick_params(labelsize=12)
plt.xticks(rotation=0)
plt.tight_layout()
plt.savefig(f'{output_dir}/02_monthly_trend_stacked.png', dpi=300, bbox_inches='tight')
print(f"Saved: 02_monthly_trend_stacked.png")
plt.close()

# Line chart - percentage
monthly_pollutants_pct = monthly_pollutants.div(monthly_pollutants.sum(axis=1), axis=0) * 100

fig, ax = plt.subplots(figsize=(18, 8))
for pollutant in monthly_pollutants_pct.columns:
    ax.plot(monthly_pollutants_pct.index, monthly_pollutants_pct[pollutant], 
            marker='o', linewidth=2.5, markersize=8, label=pollutant,
            color=colors.get(pollutant, '#95a5a6'))
ax.set_xlabel('Month', fontsize=14, fontweight='bold')
ax.set_ylabel('Percentage (%)', fontsize=14, fontweight='bold')
ax.set_title('Monthly Trend of Dominant Pollutants (Percentage)', fontsize=16, fontweight='bold')
ax.legend(title='Pollutant', title_fontsize=13, fontsize=12, loc='best')
ax.grid(True, alpha=0.3)
ax.tick_params(labelsize=12)
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig(f'{output_dir}/03_monthly_trend_percentage.png', dpi=300, bbox_inches='tight')
print(f"Saved: 03_monthly_trend_percentage.png")
plt.close()

# ============================================================================
# ANALYSIS 3: Time-of-Day (Flight) Patterns
# ============================================================================
print("\n" + "=" * 80)
print("ANALYSIS 3: Time-of-Day (Flight) Patterns")
print("=" * 80)

flight_pollutants = df.groupby(['flight_id', 'Dominant_Pollutant']).size().unstack(fill_value=0)
flight_pollutants = flight_pollutants.sort_index()

print("\nFlight Pattern:")
print(flight_pollutants)

# Heatmap
fig, ax = plt.subplots(figsize=(12, 10))
sns.heatmap(flight_pollutants.T, annot=True, fmt='d', cmap='YlOrRd', 
            linewidths=1, linecolor='white', cbar_kws={'label': 'Frequency'},
            ax=ax, annot_kws={'fontsize': 10, 'fontweight': 'bold'})
ax.set_xlabel('Flight ID', fontsize=14, fontweight='bold')
ax.set_ylabel('Dominant Pollutant', fontsize=14, fontweight='bold')
ax.set_title('Dominant Pollutant by Flight (Time of Day)', fontsize=16, fontweight='bold')
plt.tight_layout()
plt.savefig(f'{output_dir}/04_flight_pattern_heatmap.png', dpi=300, bbox_inches='tight')
print(f"Saved: 04_flight_pattern_heatmap.png")
plt.close()

# ============================================================================
# ANALYSIS 4: Spatial Distribution (by Point)
# ============================================================================
print("\n" + "=" * 80)
print("ANALYSIS 4: Spatial Distribution")
print("=" * 80)

point_pollutants = df.groupby(['point_id', 'Dominant_Pollutant']).size().unstack(fill_value=0)

print("\nSpatial Distribution by Monitoring Point:")
print(point_pollutants)

# Stacked bar chart
fig, ax = plt.subplots(figsize=(18, 8))
point_pollutants.plot(kind='bar', stacked=True, ax=ax,
                      color=[colors.get(p, '#95a5a6') for p in point_pollutants.columns],
                      edgecolor='black', linewidth=0.5)
ax.set_xlabel('Monitoring Point', fontsize=14, fontweight='bold')
ax.set_ylabel('Frequency', fontsize=14, fontweight='bold')
ax.set_title('Dominant Pollutant Distribution by Monitoring Point', fontsize=16, fontweight='bold')
ax.legend(title='Pollutant', title_fontsize=13, fontsize=12, loc='upper right')
ax.tick_params(labelsize=12)
plt.xticks(rotation=0)
plt.tight_layout()
plt.savefig(f'{output_dir}/05_spatial_distribution.png', dpi=300, bbox_inches='tight')
print(f"Saved: 05_spatial_distribution.png")
plt.close()

# ============================================================================
# ANALYSIS 5: Day of Week Pattern
# ============================================================================
print("\n" + "=" * 80)
print("ANALYSIS 5: Day of Week Pattern")
print("=" * 80)

day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
dow_pollutants = df.groupby(['day_of_week', 'Dominant_Pollutant']).size().unstack(fill_value=0)
dow_pollutants = dow_pollutants.reindex([d for d in day_order if d in dow_pollutants.index])

print("\nDay of Week Distribution:")
print(dow_pollutants)

# Grouped bar chart
fig, ax = plt.subplots(figsize=(18, 8))
dow_pollutants.plot(kind='bar', ax=ax, 
                    color=[colors.get(p, '#95a5a6') for p in dow_pollutants.columns],
                    edgecolor='black', linewidth=0.8, width=0.8)
ax.set_xlabel('Day of Week', fontsize=14, fontweight='bold')
ax.set_ylabel('Frequency', fontsize=14, fontweight='bold')
ax.set_title('Dominant Pollutant by Day of Week', fontsize=16, fontweight='bold')
ax.legend(title='Pollutant', title_fontsize=13, fontsize=12, loc='upper right')
ax.tick_params(labelsize=12)
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig(f'{output_dir}/06_day_of_week_pattern.png', dpi=300, bbox_inches='tight')
print(f"Saved: 06_day_of_week_pattern.png")
plt.close()

# ============================================================================
# ANALYSIS 6: Correlation with Temperature
# ============================================================================
print("\n" + "=" * 80)
print("ANALYSIS 6: Temperature Correlation")
print("=" * 80)

# Box plots
fig, ax = plt.subplots(figsize=(14, 8))
df.boxplot(column='Temperature (°C)', by='Dominant_Pollutant', ax=ax,
           patch_artist=True, grid=False)
plt.suptitle('')
ax.set_title('Temperature Distribution by Dominant Pollutant', fontsize=16, fontweight='bold')
ax.set_xlabel('Dominant Pollutant', fontsize=14, fontweight='bold')
ax.set_ylabel('Temperature (°C)', fontsize=14, fontweight='bold')
ax.tick_params(labelsize=12)
plt.tight_layout()
plt.savefig(f'{output_dir}/07_temperature_correlation.png', dpi=300, bbox_inches='tight')
print(f"Saved: 07_temperature_correlation.png")
plt.close()

# Average temperature by pollutant
temp_by_pollutant = df.groupby('Dominant_Pollutant')['Temperature (°C)'].agg(['mean', 'std', 'min', 'max'])
print("\nTemperature Statistics by Dominant Pollutant:")
print(temp_by_pollutant.round(2))

# ============================================================================
# ANALYSIS 7: Correlation with O2
# ============================================================================
print("\n" + "=" * 80)
print("ANALYSIS 7: Oxygen Level Correlation")
print("=" * 80)

fig, ax = plt.subplots(figsize=(14, 8))
df.boxplot(column='O2_percentage', by='Dominant_Pollutant', ax=ax,
           patch_artist=True, grid=False)
plt.suptitle('')
ax.set_title('Oxygen Level Distribution by Dominant Pollutant', fontsize=16, fontweight='bold')
ax.set_xlabel('Dominant Pollutant', fontsize=14, fontweight='bold')
ax.set_ylabel('O2 Percentage (%)', fontsize=14, fontweight='bold')
ax.tick_params(labelsize=12)
plt.tight_layout()
plt.savefig(f'{output_dir}/08_oxygen_correlation.png', dpi=300, bbox_inches='tight')
print(f"Saved: 08_oxygen_correlation.png")
plt.close()

o2_by_pollutant = df.groupby('Dominant_Pollutant')['O2_percentage'].agg(['mean', 'std', 'min', 'max'])
print("\nO2 Statistics by Dominant Pollutant:")
print(o2_by_pollutant.round(3))

# ============================================================================
# ANALYSIS 8: Weekly Time Series
# ============================================================================
print("\n" + "=" * 80)
print("ANALYSIS 8: Weekly Time Series")
print("=" * 80)

weekly_pollutants = df.groupby(['week', 'Dominant_Pollutant']).size().unstack(fill_value=0)

fig, ax = plt.subplots(figsize=(20, 8))
for pollutant in weekly_pollutants.columns:
    ax.plot(weekly_pollutants.index, weekly_pollutants[pollutant],
            marker='o', linewidth=2, markersize=6, label=pollutant,
            color=colors.get(pollutant, '#95a5a6'), alpha=0.8)
ax.set_xlabel('Week of Year', fontsize=14, fontweight='bold')
ax.set_ylabel('Frequency', fontsize=14, fontweight='bold')
ax.set_title('Weekly Time Series of Dominant Pollutants', fontsize=16, fontweight='bold')
ax.legend(title='Pollutant', title_fontsize=13, fontsize=12, loc='upper right')
ax.grid(True, alpha=0.3)
ax.tick_params(labelsize=12)
plt.tight_layout()
plt.savefig(f'{output_dir}/09_weekly_timeseries.png', dpi=300, bbox_inches='tight')
print(f"Saved: 09_weekly_timeseries.png")
plt.close()

# ============================================================================
# ANALYSIS 9: AQI Value Comparison
# ============================================================================
print("\n" + "=" * 80)
print("ANALYSIS 9: AQI Values by Dominant Pollutant")
print("=" * 80)

# Get AQI values for each dominant pollutant
aqi_data = []
for pollutant in df['Dominant_Pollutant'].unique():
    aqi_col = f"{pollutant}_AQI"
    subset = df[df['Dominant_Pollutant'] == pollutant][aqi_col]
    aqi_data.append({
        'Pollutant': pollutant,
        'Mean_AQI': subset.mean(),
        'Median_AQI': subset.median(),
        'Min_AQI': subset.min(),
        'Max_AQI': subset.max(),
        'Std_AQI': subset.std()
    })

aqi_summary = pd.DataFrame(aqi_data).sort_values('Mean_AQI', ascending=False)
print("\nAQI Statistics when each pollutant is dominant:")
print(aqi_summary.round(2))

# Violin plot
fig, ax = plt.subplots(figsize=(14, 8))
pollutant_aqi_data = []
for pollutant in df['Dominant_Pollutant'].unique():
    aqi_col = f"{pollutant}_AQI"
    pollutant_aqi_data.append(df[df['Dominant_Pollutant'] == pollutant][aqi_col].values)

parts = ax.violinplot(pollutant_aqi_data, positions=range(len(df['Dominant_Pollutant'].unique())),
                      showmeans=True, showmedians=True)
ax.set_xticks(range(len(df['Dominant_Pollutant'].unique())))
ax.set_xticklabels(df['Dominant_Pollutant'].unique())
ax.set_xlabel('Dominant Pollutant', fontsize=14, fontweight='bold')
ax.set_ylabel('AQI Value', fontsize=14, fontweight='bold')
ax.set_title('AQI Distribution when Each Pollutant is Dominant', fontsize=16, fontweight='bold')
ax.grid(True, alpha=0.3, axis='y')
ax.tick_params(labelsize=12)
plt.tight_layout()
plt.savefig(f'{output_dir}/10_aqi_comparison.png', dpi=300, bbox_inches='tight')
print(f"Saved: 10_aqi_comparison.png")
plt.close()

# ============================================================================
# ANALYSIS 10: Seasonal Analysis
# ============================================================================
print("\n" + "=" * 80)
print("ANALYSIS 10: Seasonal Analysis")
print("=" * 80)

# Define seasons
def get_season(month):
    if month in [12, 1, 2]:
        return 'Winter'
    elif month in [3, 4, 5]:
        return 'Spring'
    elif month in [6, 7, 8, 9]:
        return 'Monsoon'
    else:
        return 'Autumn'

df['season'] = df['month'].apply(get_season)

seasonal_pollutants = df.groupby(['season', 'Dominant_Pollutant']).size().unstack(fill_value=0)
season_order = ['Winter', 'Spring', 'Monsoon', 'Autumn']
seasonal_pollutants = seasonal_pollutants.reindex([s for s in season_order if s in seasonal_pollutants.index])

print("\nSeasonal Distribution:")
print(seasonal_pollutants)

fig, ax = plt.subplots(figsize=(14, 8))
seasonal_pollutants.plot(kind='bar', ax=ax,
                         color=[colors.get(p, '#95a5a6') for p in seasonal_pollutants.columns],
                         edgecolor='black', linewidth=1, width=0.7)
ax.set_xlabel('Season', fontsize=14, fontweight='bold')
ax.set_ylabel('Frequency', fontsize=14, fontweight='bold')
ax.set_title('Seasonal Distribution of Dominant Pollutants', fontsize=16, fontweight='bold')
ax.legend(title='Pollutant', title_fontsize=13, fontsize=12, loc='upper right')
ax.tick_params(labelsize=12)
plt.xticks(rotation=0)
plt.tight_layout()
plt.savefig(f'{output_dir}/11_seasonal_analysis.png', dpi=300, bbox_inches='tight')
print(f"Saved: 11_seasonal_analysis.png")
plt.close()

# ============================================================================
# FINAL SUMMARY
# ============================================================================
print("\n" + "=" * 80)
print("ANALYSIS COMPLETE!")
print("=" * 80)

summary_text = f"""
COMPREHENSIVE TREND ANALYSIS SUMMARY
{'='*80}

Total Measurements: {len(df):,}
Date Range: {df['timestamp'].min()} to {df['timestamp'].max()}

Most Dominant Pollutant: {pollutant_counts.index[0]} ({pollutant_pct.iloc[0]:.1f}%)
Least Dominant Pollutant: {pollutant_counts.index[-1]} ({pollutant_pct.iloc[-1]:.1f}%)

All visualizations saved in: {output_dir}/

Files Created:
  01. Overall distribution (bar & pie charts)
  02. Monthly trend (stacked bar chart)
  03. Monthly trend (percentage line chart)
  04. Flight pattern heatmap
  05. Spatial distribution by point
  06. Day of week pattern
  07. Temperature correlation
  08. Oxygen level correlation
  09. Weekly time series
  10. AQI value comparison
  11. Seasonal analysis

Key Findings:
  - NOx dominates in {pollutant_pct.get('NOx', 0):.1f}% of cases
  - Spatial variation exists across 15 monitoring points
  - Temporal patterns show variations by time of day, day of week, and season
  - Correlations with temperature and O2 levels identified
"""

print(summary_text)

# Save summary to file
with open(f'{output_dir}/ANALYSIS_SUMMARY.txt', 'w') as f:
    f.write(summary_text)
    f.write("\n\nDetailed Statistics:\n")
    f.write("="*80 + "\n")
    f.write("\nOverall Distribution:\n")
    f.write(pollutant_counts.to_string())
    f.write("\n\nTemperature by Pollutant:\n")
    f.write(temp_by_pollutant.to_string())
    f.write("\n\nO2 by Pollutant:\n")
    f.write(o2_by_pollutant.to_string())
    f.write("\n\nAQI Summary:\n")
    f.write(aqi_summary.to_string())

print(f"\nSummary saved to: {output_dir}/ANALYSIS_SUMMARY.txt")
print("\n" + "=" * 80)

