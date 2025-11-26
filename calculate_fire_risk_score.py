import pandas as pd
import numpy as np
import os

# Change to the correct directory
os.chdir(r'C:\Users\Abhijit\OneDrive - iitkgp.ac.in\Desktop\Gupta_BTP')

print("=" * 80)
print("CALCULATING FIRE RISK SCORE (FRS)")
print("=" * 80)

# Read the CSV
df = pd.read_csv('Untitled spreadsheet - opencast_15points_12flights_dataset.csv')

print(f"\nLoaded data: {len(df):,} rows")
print(f"Current columns: {len(df.columns)}")

# Molecular weights for conversion
MW_CO = 28.01
MW_CH4 = 16.04
CONVERSION_FACTOR = 24.45  # At standard conditions

print("\nStep 1: Converting concentrations to ppm")
print("-" * 80)

# Convert CO from ug/m3 to ppm
df['CO_ppm'] = df['CO_ug_m3'] / ((MW_CO / CONVERSION_FACTOR) * 1000)

# Convert CH4 from ug/m3 to ppm
df['CH4_ppm'] = df['CH4_ug_m3'] / ((MW_CH4 / CONVERSION_FACTOR) * 1000)

print(f"CO_ppm range: {df['CO_ppm'].min():.2f} - {df['CO_ppm'].max():.2f}")
print(f"CH4_ppm range: {df['CH4_ppm'].min():.2f} - {df['CH4_ppm'].max():.2f}")

print("\nStep 2: Calculating normalized values")
print("-" * 80)

# Function to clamp values between 0 and 1
def clamp(value, min_val=0, max_val=1):
    return np.clip(value, min_val, max_val)

# Calculate norm_GR
# norm_GR = clamp((log10(GR) + 1) / 3, 0, 1)
def calculate_norm_GR(gr):
    if gr <= 0:
        return 0.0
    return clamp((np.log10(gr) + 1) / 3, 0, 1)

df['norm_GR'] = df['GR'].apply(calculate_norm_GR)

# Calculate norm_CO
# norm_CO = clamp((CO_ppm - 5) / (200 - 5), 0, 1)
df['norm_CO'] = clamp((df['CO_ppm'] - 5) / (200 - 5), 0, 1)

# Calculate norm_CH4
# norm_CH4 = clamp((CH4_ppm - 1) / (100 - 1), 0, 1)
df['norm_CH4'] = clamp((df['CH4_ppm'] - 1) / (100 - 1), 0, 1)

print(f"norm_GR range: {df['norm_GR'].min():.4f} - {df['norm_GR'].max():.4f}")
print(f"norm_CO range: {df['norm_CO'].min():.4f} - {df['norm_CO'].max():.4f}")
print(f"norm_CH4 range: {df['norm_CH4'].min():.4f} - {df['norm_CH4'].max():.4f}")

print("\nStep 3: Calculating Fire Risk Score (FRS)")
print("-" * 80)

# Define weights (these are typical for underground mining)
# GR is the most important indicator, followed by CO and CH4
w_GR = 0.5   # Graham's Ratio - primary indicator
w_CO = 0.3   # Carbon Monoxide - combustion indicator
w_CH4 = 0.2  # Methane - explosive gas indicator

print(f"Weights: w_GR={w_GR}, w_CO={w_CO}, w_CH4={w_CH4}")
print(f"Total weight: {w_GR + w_CO + w_CH4} (should be 1.0)")

# Calculate FRS
# FRS = 100 × (w_GR · norm_GR + w_CO · norm_CO + w_CH4 · norm_CH4)
df['FRS'] = 100 * (w_GR * df['norm_GR'] + w_CO * df['norm_CO'] + w_CH4 * df['norm_CH4'])

# Round to 2 decimal places
df['FRS'] = df['FRS'].round(2)
df['norm_GR'] = df['norm_GR'].round(4)
df['norm_CO'] = df['norm_CO'].round(4)
df['norm_CH4'] = df['norm_CH4'].round(4)
df['CO_ppm'] = df['CO_ppm'].round(3)
df['CH4_ppm'] = df['CH4_ppm'].round(3)

print(f"\nFRS calculated successfully!")
print(f"FRS range: {df['FRS'].min():.2f} - {df['FRS'].max():.2f}")

# Save the updated CSV
df.to_csv('Untitled spreadsheet - opencast_15points_12flights_dataset.csv', index=False)

print(f"\nSaved updated data with new columns")

# Generate statistics
print("\n" + "=" * 80)
print("FIRE RISK SCORE (FRS) STATISTICS")
print("=" * 80)

print(f"\nOverall FRS Statistics:")
print(f"  Mean:   {df['FRS'].mean():.2f}")
print(f"  Median: {df['FRS'].median():.2f}")
print(f"  Min:    {df['FRS'].min():.2f}")
print(f"  Max:    {df['FRS'].max():.2f}")
print(f"  Std Dev: {df['FRS'].std():.2f}")

# FRS Risk Categories
def frs_category(frs):
    if frs < 20:
        return "Low Risk"
    elif frs < 40:
        return "Moderate Risk"
    elif frs < 60:
        return "High Risk"
    elif frs < 80:
        return "Very High Risk"
    else:
        return "Critical Risk"

df['FRS_Category'] = df['FRS'].apply(frs_category)

print("\n" + "=" * 80)
print("FIRE RISK SCORE DISTRIBUTION")
print("=" * 80)

category_counts = df['FRS_Category'].value_counts()
category_percentages = (category_counts / len(df) * 100).round(2)

print("\nFRS Category Distribution:")
for category in ["Low Risk", "Moderate Risk", "High Risk", "Very High Risk", "Critical Risk"]:
    if category in category_counts.index:
        count = category_counts[category]
        percentage = category_percentages[category]
        print(f"  {category:20s}: {count:6,} ({percentage:5.2f}%)")

# Sample data
print("\n" + "=" * 80)
print("SAMPLE DATA WITH FRS")
print("=" * 80)

sample_cols = ['timestamp', 'point_id', 'GR', 'CO_ppm', 'CH4_ppm', 'norm_GR', 'norm_CO', 'norm_CH4', 'FRS']
print("\nFirst 10 rows:")
print(df[sample_cols].head(10).to_string(index=False))

# Show extreme cases
print("\n\nHighest Fire Risk (Top 5):")
highest_frs = df.nlargest(5, 'FRS')[['timestamp', 'point_id', 'GR', 'CO_ppm', 'CH4_ppm', 'FRS', 'Temperature (°C)', 'O2_percentage']]
print(highest_frs.to_string(index=False))

print("\n\nLowest Fire Risk (Bottom 5):")
lowest_frs = df.nsmallest(5, 'FRS')[['timestamp', 'point_id', 'GR', 'CO_ppm', 'CH4_ppm', 'FRS', 'Temperature (°C)', 'O2_percentage']]
print(lowest_frs.to_string(index=False))

# Correlation analysis
print("\n" + "=" * 80)
print("CORRELATION ANALYSIS")
print("=" * 80)

correlations = {
    'GR': df['FRS'].corr(df['GR']),
    'CO_ppm': df['FRS'].corr(df['CO_ppm']),
    'CH4_ppm': df['FRS'].corr(df['CH4_ppm']),
    'Temperature': df['FRS'].corr(df['Temperature (°C)']),
    'O2_percentage': df['FRS'].corr(df['O2_percentage']),
}

print("\nCorrelation with FRS:")
for factor, corr in correlations.items():
    print(f"  {factor:15s}: {corr:7.4f}")

# Average FRS by location
print("\n" + "=" * 80)
print("FIRE RISK BY MONITORING POINT")
print("=" * 80)

point_frs = df.groupby('point_id')['FRS'].agg(['mean', 'min', 'max', 'std']).round(2)
print("\nAverage FRS by Point:")
print(point_frs.sort_values('mean', ascending=False))

# Remove temporary category column before final save
df = df.drop('FRS_Category', axis=1)
df.to_csv('Untitled spreadsheet - opencast_15points_12flights_dataset.csv', index=False)

print("\n" + "=" * 80)
print("FIRE RISK SCORE (FRS) CALCULATION COMPLETE!")
print("=" * 80)

print("\nNew columns added:")
print("  1. CO_ppm        - CO in parts per million")
print("  2. CH4_ppm       - CH4 in parts per million")
print("  3. norm_GR       - Normalized Graham's Ratio (0-1)")
print("  4. norm_CO       - Normalized CO (0-1)")
print("  5. norm_CH4      - Normalized CH4 (0-1)")
print("  6. FRS           - Fire Risk Score (0-100)")

print("\nFRS Interpretation:")
print("  0-20:  Low Risk         - Normal conditions")
print("  20-40: Moderate Risk    - Monitor closely")
print("  40-60: High Risk        - Increased vigilance required")
print("  60-80: Very High Risk   - Immediate attention needed")
print("  80-100: Critical Risk   - Emergency response required")

print("\nFormulas used:")
print("  norm_GR = clamp((log10(GR) + 1) / 3, 0, 1)")
print("  norm_CO = clamp((CO_ppm - 5) / (200 - 5), 0, 1)")
print("  norm_CH4 = clamp((CH4_ppm - 1) / (100 - 1), 0, 1)")
print(f"  FRS = 100 × ({w_GR}·norm_GR + {w_CO}·norm_CO + {w_CH4}·norm_CH4)")

print("\n" + "=" * 80)

