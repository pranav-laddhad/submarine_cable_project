import pandas as pd

# Load the CSV file
with open("telegeography_data.csv", 'r', encoding='utf-8') as file:
    lines = file.readlines()

# Find the line where the header starts (based on column names)
header_line = None
for i, line in enumerate(lines):
    if "Cable" in line and "Region" in line and "Fault Location" in line:
        header_line = i
        break

# If header line is found, reload the CSV with the proper header line and skip unwanted rows
if header_line is not None:
    df = pd.read_csv("telegeography_data.csv", header=header_line)
    
    # Add the 'Final Inferred Category' column with all 'NA' values
    df['Final Inferred Category'] = 'NA'
    
    # Save the updated DataFrame back to a new CSV file
    df.to_csv("telegeography_data_updated.csv", index=False)
    print("Column 'Final Inferred Category' added with 'NA' values and cleaned data saved.")
else:
    print("Header row not found.")
