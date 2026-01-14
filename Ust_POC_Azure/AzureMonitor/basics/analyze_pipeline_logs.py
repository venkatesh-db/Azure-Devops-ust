import re
from datetime import datetime

# File paths
log_file_path = "azure_devops_pipeline_logs.txt"
report_file_path = "pipeline_analysis_report.txt"

# Function to parse logs
def parse_logs(file_path):
    logs = []
    with open(file_path, "r") as file:
        for line in file:
            timestamp_match = re.match(r"(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d{3}Z): (.+)", line)
            if timestamp_match:
                timestamp = datetime.strptime(timestamp_match.group(1), "%Y-%m-%dT%H:%M:%S.%fZ")
                message = timestamp_match.group(2)
                logs.append({"timestamp": timestamp, "message": message})
    return logs

# Function to analyze logs
def analyze_logs(logs):
    issues = []
    for log in logs:
        if "error" in log["message"].lower() or "failed" in log["message"].lower():
            issues.append(log)
    return issues

# Function to generate a report
def generate_report(issues, output_path):
    with open(output_path, "w") as file:
        if not issues:
            file.write("No issues detected in the pipeline logs.\n")
        else:
            file.write("Root Cause Analysis Report:\n")
            file.write("===========================\n")
            for issue in issues:
                file.write(f"{issue['timestamp']}: {issue['message']}\n")

# Main execution
if __name__ == "__main__":
    logs = parse_logs(log_file_path)
    issues = analyze_logs(logs)
    generate_report(issues, report_file_path)
    print(f"Analysis complete. Report generated at: {report_file_path}")