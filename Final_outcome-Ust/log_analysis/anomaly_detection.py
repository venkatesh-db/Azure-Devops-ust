import pandas as pd
from sklearn.ensemble import IsolationForest

def detect_anomalies(log_data, value_column):
    """
    Detect anomalies in log data using Isolation Forest.

    Args:
        log_data (pd.DataFrame): Log data as a DataFrame.
        value_column (str): Name of the value column.

    Returns:
        pd.DataFrame: Log data with an additional 'Anomaly' column.
    """
    model = IsolationForest(contamination=0.05, random_state=42)
    log_data['Anomaly'] = model.fit_predict(log_data[[value_column]])
    return log_data

# Example usage
if __name__ == "__main__":
    log_file_path = "/Users/venkatesh/Devops-GenAI_UST/Final Projects/ustlogs/log_analysis/dummy_logs.csv"
    log_data = pd.read_csv(log_file_path, parse_dates=['TimeGenerated'])

    result = detect_anomalies(log_data, 'Value')
    print(result)