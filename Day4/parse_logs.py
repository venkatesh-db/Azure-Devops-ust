import os
import pandas as pd
import requests

# Directory containing server logs
LOG_DIR = "logs"

# Function to parse server logs
def parse_logs():
    data = []
    for file_name in os.listdir(LOG_DIR):
        if file_name.endswith(".log"):
            with open(os.path.join(LOG_DIR, file_name), 'r') as file:
                for line in file:
                    # Example: Parse log lines (customize as needed)
                    parts = line.strip().split()
                    if len(parts) > 3:
                        data.append({
                            "timestamp": parts[0],
                            "level": parts[1],
                            "message": " ".join(parts[2:])
                        })
    return pd.DataFrame(data)

# Function to load data to Power BI
def load_to_power_bi(dataframe):
    # Example: Power BI REST API endpoint
    power_bi_url = "https://api.powerbi.com/beta/..."
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer YOUR_ACCESS_TOKEN"
    }
    response = requests.post(power_bi_url, headers=headers, json=dataframe.to_dict(orient='records'))
    if response.status_code == 200:
        print("Data successfully loaded to Power BI.")
    else:
        print(f"Failed to load data: {response.status_code}, {response.text}")

if __name__ == "__main__":
    # Parse logs
    df = parse_logs()
    print("Parsed Data:")
    print(df.head())

    # Load to Power BI
    load_to_power_bi(df)