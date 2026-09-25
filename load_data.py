import glob, os
import pandas as pd
from sqlalchemy import create_engine

#Read Password from environment variable
password = os.environ.get('PG_PASSWORD')
engine = create_engine(f'postgresql://postgres:{password}@localhost:5432/olist')

# Load data from CSV files into PostgreSQL database
for file in glob.glob('data/*.csv'):
    name = (os.path.basename(file).replace("olist_", "")
            .replace("_dataset", "").replace(".csv", ""))
    df = pd.read_csv(file,encoding="utf-8-sig")

    for col in df.columns:
        if "date" in col or "timestamp" in col:
            df[col] = pd.to_datetime(df[col], errors='coerce')

    #Write to PostgreSQL database, replacing the table if it already exists
    df.to_sql(name, engine, if_exists='replace', index=False,chunksize=10000)
    print(f"Loaded {name} into PostgreSQL database.",len(df), "rows.")
