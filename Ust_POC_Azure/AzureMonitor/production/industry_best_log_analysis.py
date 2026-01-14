import os
import re
from datetime import datetime

# Define constants for log and report paths
LOG_FOLDER = "production"
LOG_FILE_NAME = "log_analytics_workspace_logs.txt"
LOG_FILE_PATH = os.path.join(LOG_FOLDER, LOG_FILE_NAME)
REPORT_FILE_NAME = "detailed_pipeline_analysis_report.txt"
REPORT_FILE_PATH = os.path.join(LOG_FOLDER, REPORT_FILE_NAME)

# Function to parse logs
def parse_logs(file_path):
    """Parse logs and extract timestamped messages."""
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
    """Analyze logs to identify recurring issues and failures."""
    issues = []
    recurring_issues = {}

    for log in logs:
        message = log["message"].lower()
        if "error" in message or "failed" in message:
            issues.append(log)

            # Track recurring issues
            if message not in recurring_issues:
                recurring_issues[message] = 0
            recurring_issues[message] += 1

    return issues, recurring_issues

# Function to generate a detailed report
def generate_report(issues, recurring_issues, output_path):
    """Generate a detailed analysis report."""
    with open(output_path, "w") as file:
        file.write("Detailed Pipeline Analysis Report\n")
        file.write("================================\n\n")

        # Write identified issues
        if not issues:
            file.write("No issues detected in the pipeline logs.\n\n")
        else:
            file.write("Identified Issues:\n")
            for issue in issues:
                file.write(f"{issue['timestamp']}: {issue['message']}\n")
            file.write("\n")

        # Write recurring issues
        if recurring_issues:
            file.write("Recurring Issues:\n")
            for issue, count in recurring_issues.items():
                file.write(f"- {issue.capitalize()} (Occurred {count} times)\n")
            file.write("\n")

        # Write AI-based recommendations
        file.write("AI-Based Recommendations:\n")
        for issue, count in recurring_issues.items():
            if "nullpointerexception" in issue:
                file.write("- NullPointerException: Check for uninitialized variables in the code.\n")
            elif "timeout" in issue:
                file.write("- Timeout: Investigate network latency and increase timeout thresholds.\n")
            elif "memory leak" in issue:
                file.write("- Memory Leak: Ensure proper resource deallocation and close database connections.\n")
        file.write("\n")

        file.write("End of Report\n")

# Main execution
def main():
    """Main function to execute the log analysis pipeline."""
    if not os.path.exists(LOG_FILE_PATH):
        print(f"Log file not found: {LOG_FILE_PATH}")
        return

    logs = parse_logs(LOG_FILE_PATH)
    issues, recurring_issues = analyze_logs(logs)
    generate_report(issues, recurring_issues, REPORT_FILE_PATH)
    print(f"Analysis complete. Report generated at: {REPORT_FILE_PATH}")

if __name__ == "__main__":
    main()