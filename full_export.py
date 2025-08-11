import requests
import pandas as pd
from tqdm import tqdm

DUNE_API_KEY = "[YOUR_DUNE_API_KEY]"
QUERY_ID = [YOUR_QUERY_ID]
LIMIT = 10000
BASE_URL = "https://api.dune.com/api/v1"
CSV_FILE = "[DESIRED_FILENAME].csv"

headers = {
    "x-dune-api-key": DUNE_API_KEY
}

meta_url = f"{BASE_URL}/query/{QUERY_ID}/results"
meta_resp = requests.get(meta_url, headers=headers)
meta_resp.raise_for_status()
meta_data = meta_resp.json()

try:
    total_rows = meta_data['result']['metadata']['total_row_count']
except KeyError:
    print("⚠️ Warning: Could not find total_row_count. Defaulting to first-page fetch.")
    total_rows = LIMIT

try:
    columns = [col['name'] for col in meta_data['result']['metadata']['columns']]
except KeyError:
    print("⚠️ Warning: 'columns' not found in metadata. Inferring from first page...")
    first_rows = meta_data['result']['rows']
    if not first_rows:
        raise ValueError("No rows found in result.")
    columns = list(first_rows[0].keys())

print(f"➡️ Total rows to fetch: {total_rows}")
print(f"➡️ Columns: {columns}")

all_rows = []

for offset in tqdm(range(0, total_rows, LIMIT), desc="Downloading data"):
    page_url = f"{BASE_URL}/query/{QUERY_ID}/results?limit={LIMIT}&offset={offset}"
    page_resp = requests.get(page_url, headers=headers)
    page_resp.raise_for_status()
    rows = page_resp.json()['result']['rows']
    if not rows:
        break
    all_rows.extend(rows)

df = pd.DataFrame(all_rows, columns=columns)
df.to_csv(CSV_FILE, index=False)
print(f"✅ Saved full dataset to: {CSV_FILE}")
