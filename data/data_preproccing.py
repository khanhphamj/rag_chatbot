# Clean and prepare the data for PostgreSQL import
import pandas as pd

df_latest = pd.read_excel('laptop_all.xlsx')

# Select and rename columns to match PostgreSQL schema
df_latest = df_latest[['name', 'price', 'ram', 'rom_type', 'rom',
                       'screen_size', 'screen_detail', 'cpu', 'gpu', 'battery', 'weight',
                       'rating', 'links_href', 'brand', 'series', 'is_laptopai', 'is_laptopgaming']]

# Rename 'links-href' to 'link_href'

# Ensure correct data types
df_latest['ram'] = pd.to_numeric(df_latest['ram'], errors='coerce').fillna(0).astype(int)
df_latest['rom'] = pd.to_numeric(df_latest['rom'], errors='coerce').fillna(0).astype(int)
df_latest['screen_size'] = pd.to_numeric(df_latest['screen_size'], errors='coerce').fillna(0.0).astype(float)
df_latest['weight'] = pd.to_numeric(df_latest['weight'], errors='coerce').fillna(0.0).astype(float)
df_latest['rating'] = pd.to_numeric(df_latest['rating'], errors='coerce').fillna(0.0).astype(float)
df_latest['is_laptopai'] = df_latest['is_laptopai'].astype(bool)
df_latest['is_laptopgaming'] = df_latest['is_laptopgaming'].astype(bool)

# Save the cleaned DataFrame as a CSV file
csv_file_path_latest = 'laptop_all_clean.csv'
df_latest.to_csv(csv_file_path_latest, index=False)
print("✅ Excel file successfully cleaned and saved as CSV.")

