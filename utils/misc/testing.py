import pandas as pd

file_path = "locations.xlsx"
df = pd.read_excel(file_path)
print(df['Unnamed: 5'])
