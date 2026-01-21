import pandas as pd
import matplotlib.pyplot as plt

def detect_trends(log_data, time_column, value_column):
    """
    Detect trends in log data.

    Args:
        log_data (pd.DataFrame): Log data as a DataFrame.
        time_column (str): Name of the time column.
        value_column (str): Name of the value column.

    Returns:
        None: Displays a trend plot.
    """
    log_data[time_column] = pd.to_datetime(log_data[time_column])
    log_data = log_data.sort_values(by=time_column)

    plt.figure(figsize=(10, 6))
    plt.plot(log_data[time_column], log_data[value_column], label='Trend')
    plt.xlabel('Time')
    plt.ylabel('Value')
    plt.title('Trend Detection')
    plt.legend()
    plt.grid()
    plt.show()

# Example usage
if __name__ == "__main__":
    log_file_path = "/Users/venkatesh/Devops-GenAI_UST/Final Projects/ustlogs/log_analysis/dummy_logs.csv"
    log_data = pd.read_csv(log_file_path, parse_dates=['TimeGenerated'])

    detect_trends(log_data, 'TimeGenerated', 'Value')