import sqlite3
import pandas as pd
import json

conn = sqlite3.connect('C:/Users/amehr/.gemini/antigravity/brain/2d7dcea9-02af-4ae3-93a7-88b5d217683c/bangalore_companies.db')

# Export companies table
df_companies = pd.read_sql('SELECT * FROM companies', conn)
df_companies.to_csv('C:/Users/amehr/.gemini/antigravity/brain/2d7dcea9-02af-4ae3-93a7-88b5d217683c/bangalore_companies_database.csv', index=False)
df_companies.to_json('C:/Users/amehr/.gemini/antigravity/brain/2d7dcea9-02af-4ae3-93a7-88b5d217683c/bangalore_companies_database.json', orient='records', indent=2)

# Export enterprise_deep_dives table
df_dives = pd.read_sql('SELECT * FROM enterprise_deep_dives', conn)
df_dives.to_csv('C:/Users/amehr/.gemini/antigravity/brain/2d7dcea9-02af-4ae3-93a7-88b5d217683c/enterprise_deep_dives.csv', index=False)
df_dives.to_json('C:/Users/amehr/.gemini/antigravity/brain/2d7dcea9-02af-4ae3-93a7-88b5d217683c/enterprise_deep_dives.json', orient='records', indent=2)

print('Exported both tables successfully!')
print(f'Companies count: {len(df_companies)}, Deep dives count: {len(df_dives)}')
conn.close()
