# Azure Log Analytics Integration

import logging
import requests
import os

def setup_logging():
    """
    Set up logging to integrate with Azure Log Analytics.
    """
    workspace_id = os.getenv("AZURE_WORKSPACE_ID")
    shared_key = os.getenv("AZURE_SHARED_KEY")

    if not workspace_id or not shared_key:
        logging.error("Azure Log Analytics credentials are not set in environment variables.")
        return

    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    logging.info("Azure Log Analytics integration initialized.")

    # Example: Send a test log to Azure Log Analytics
    log_data = {
        "message": "Test log for Azure Log Analytics",
        "level": "INFO"
    }
    send_log_to_azure(workspace_id, shared_key, log_data)

def send_log_to_azure(workspace_id, shared_key, log_data):
    """
    Send logs to Azure Log Analytics.

    Args:
        workspace_id (str): Azure Log Analytics workspace ID.
        shared_key (str): Azure Log Analytics shared key.
        log_data (dict): Log data to send.
    """
    url = f"https://{workspace_id}.ods.opinsights.azure.com/api/logs?api-version=2016-04-01"
    headers = {
        "Content-Type": "application/json",
        "Log-Type": "PipelineLogs",
        "Authorization": f"SharedKey {workspace_id}:{shared_key}"
    }
    try:
        response = requests.post(url, json=log_data, headers=headers)
        if response.status_code == 200:
            logging.info("Log successfully sent to Azure Log Analytics.")
        else:
            logging.error(f"Failed to send log: {response.status_code} - {response.text}")
    except requests.RequestException as e:
        logging.error(f"Error sending log to Azure Log Analytics: {e}")

# Example usage
if __name__ == "__main__":
    setup_logging()