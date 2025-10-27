import pandas as pd

df = pd.read_csv("RustFlakyTest/issues-ftw25-artifact.csv")

root_cause_category = df['root_cause_category'].dropna().unique()

print(len(root_cause_category))
print(root_cause_category)
