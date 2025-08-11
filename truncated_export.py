import requests
import pandas as pd
from tqdm import tqdm

DUNE_API_KEY = "[YOUR_DUNE_API_KEY]"
QUERY_ID = [YOUR_QUERY_ID]
MAX_ROWS = [DESIRED_MAX_ROWS]
SORT_ORDER = "[ASC_OR_DESC]"
SORT_COLUMN = "[SORT_COLUMN_NAME]"
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
    rows_to_fetch = min(total_rows, MAX_ROWS)
except KeyError:
    print("⚠️ Warning: Could not find total_row_count. Fetching up to MAX_ROWS.")
    rows_to_fetch = MAX_ROWS

try:
    columns = [col['name'] for col in meta_data['result']['metadata']['columns']]
except KeyError:
    print("⚠️ Warning: 'columns' not found in metadata. Inferring from first page...")
    first_rows = meta_data['result']['rows']
    if not first_rows:
        raise ValueError("No rows found in result.")
    columns = list(first_rows[0].keys())

print(f"➡️ Total rows available: {total_rows if 'total_rows' in locals() else 'Unknown'}")
print(f"➡️ Rows to fetch: {rows_to_fetch}")
print(f"➡️ Columns: {columns}")

all_rows = []
fetched_rows = 0

for offset in tqdm(range(0, rows_to_fetch, LIMIT), desc="Downloading data"):
    remaining_rows = rows_to_fetch - fetched_rows
    current_limit = min(LIMIT, remaining_rows)
    
    if current_limit <= 0:
        break
    
    sort_param = f"{SORT_COLUMN} {SORT_ORDER}" if SORT_COLUMN and SORT_ORDER else ""
    page_url = f"{BASE_URL}/query/{QUERY_ID}/results?limit={current_limit}&offset={offset}"
    if sort_param:
        page_url += f"&sort_by={sort_param}"
    page_resp = requests.get(page_url, headers=headers)
    page_resp.raise_for_status()
    rows = page_resp.json()['result']['rows']
    
    if not rows:
        break
    
    all_rows.extend(rows)
    fetched_rows += len(rows)
    
    if fetched_rows >= MAX_ROWS:
        break

df = pd.DataFrame(all_rows[:MAX_ROWS], columns=columns)
df.to_csv(CSV_FILE, index=False)
print(f"✅ Saved {len(df)} rows to: {CSV_FILE}")
