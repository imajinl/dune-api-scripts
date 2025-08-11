# Dune API Scripts

Python scripts for extracting and analyzing data from Dune Analytics API with support for full dataset exports and truncated exports with sorting capabilities.

## Installation

Install the required dependencies:

```bash
pip install -r scripts/requirements.txt
```

## Scripts

### 1. Full Export Script (`scripts/full_export.py`)

Downloads the complete dataset from a Dune query and saves it to CSV.

**Usage:**
1. Replace `[YOUR_DUNE_API_KEY]` with your actual Dune API key
2. Replace `[YOUR_QUERY_ID]` with your query ID (numeric)
3. Replace `[DESIRED_FILENAME].csv` with your desired output filename

### 2. Truncated Export Script (`scripts/truncated_export.py`)

Downloads a limited number of rows from a Dune query with optional sorting capabilities.

**Parameters:**
- `DUNE_API_KEY`: Your Dune Analytics API key
- `QUERY_ID`: Numeric ID of your saved Dune query
- `MAX_ROWS`: Maximum number of rows to fetch
- `SORT_ORDER`: Either "ASC" (ascending) or "DESC" (descending)
- `SORT_COLUMN`: Column name to sort by (e.g., "block_hour")
- `CSV_FILE`: Output filename

**Sorting Options:**
The SORT_ORDER parameter controls the direction of data retrieval. Use "DESC" (descending) to get the most recent or highest values first, which is ideal for getting the latest transactions, blocks, or timestamps. Use "ASC" (ascending) to get the oldest or lowest values first. The SORT_COLUMN must match an existing column name in your query results exactly (e.g., 'block_hour').

Also note that many queries don't have one row per day (for instance, some queries may collect data in granular hour increments. Accordingly, the desired max row parameter needs to be adjusted.

## Important Notes

Text in **square brackets** (e.g., [YOUR_DUNE_API_KEY]) represents **placeholders** that you must replace with your actual values. 

### Pricing Information

Dune's API charges based on the amount of data retrieved, not the number of requests. Each API call consumes credits according to the number of datapoints returned, where a datapoint is defined as either one cell of data or every 100 bytes, whichever is greater. The rate is 1 credit per 1,000 datapoints. This script fetches cached query results and does not trigger new executions, avoiding the 20-credit execution cost.

### API Rate Limits

- Free tier: 40 requests per minute
- Plus tier: 200 requests per minute  
- Premium tier: 1000 requests per minute

## Example Usage

```python
# Example configuration for truncated_export.py
DUNE_API_KEY = "your_api_key_here"
QUERY_ID = 1234567
MAX_ROWS = 1000
SORT_ORDER = "DESC"
SORT_COLUMN = "block_time"
CSV_FILE = "latest_1000_transactions.csv"
```

This configuration would fetch the 1000 most recent transactions based on block_time.

## Examples

The `examples/` directory contains sample analysis scripts showing how to process and visualize the exported data.

## Requirements

- Python 3.7+
- requests
- pandas
- tqdm
- matplotlib (for examples)

## Setting Up Python Environment

### Windows

```bash
# Install Python from python.org or Microsoft Store
# Create virtual environment
python -m venv dune-env
dune-env\Scripts\activate
pip install -r scripts/requirements.txt
```

### macOS

```bash
# Install Python via Homebrew (recommended)
brew install python
# Create virtual environment
python3 -m venv dune-env
source dune-env/bin/activate
pip install -r scripts/requirements.txt
```

### Linux (Ubuntu / Debian)

```bash
# Install Python and pip
sudo apt update
sudo apt install python3 python3-pip python3-venv
# Create virtual environment
python3 -m venv dune-env
source dune-env/bin/activate
pip install -r scripts/requirements.txt
```

### Deactivating Environment

To deactivate the virtual environment when done:
```bash
deactivate
```

### Using Jupyter Notebook

If you prefer to run the scripts in Jupyter Notebook:

```bash
# After activating your virtual environment, install Jupyter
pip install jupyter

# Start Jupyter Notebook
jupyter notebook

# In the notebook, install packages directly:
!pip install requests pandas tqdm matplotlib

# Then copy and paste the script code into notebook cells
```

## License

MIT License
