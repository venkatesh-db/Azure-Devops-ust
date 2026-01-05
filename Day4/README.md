# Parse Server Logs and Load Insights to Power BI

## Overview
This project is designed to parse server logs using Python, extract meaningful insights, and load the data into Power BI for visualization.

## Steps
1. Parse server logs to extract relevant data.
2. Transform the data into a format suitable for Power BI.
3. Load the data into Power BI using the Power BI REST API or other integration methods.

## Requirements
- Python 3.8+
- Required libraries: pandas, requests, etc.

## Setup
1. Install the required libraries:
   ```bash
   pip install pandas requests
   ```
2. Run the script to parse logs and load data.

## Usage
- Place your server logs in the `logs/` directory.
- Run the script:
  ```bash
  python parse_logs.py
  ```