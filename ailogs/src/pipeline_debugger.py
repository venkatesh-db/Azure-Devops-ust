import logging
import os

class PipelineDebugger:
    def __init__(self, log_dir):
        self.log_dir = log_dir
        self.logs = []

    def load_logs(self):
        """Load logs from the specified directory."""
        try:
            for file_name in os.listdir(self.log_dir):
                if file_name.endswith(".log"):
                    with open(os.path.join(self.log_dir, file_name), "r") as file:
                        self.logs.append(file.read())
        except Exception as e:
            logging.error(f"Error loading logs: {e}")

    def parse_logs(self):
        """Parse logs to identify errors and bottlenecks."""
        parsed_data = []
        for log in self.logs:
            if "ERROR" in log or "FAIL" in log:
                parsed_data.append(log)
        return parsed_data

    def debug_pipeline(self):
        """Main method to debug the pipeline."""
        self.load_logs()
        errors = self.parse_logs()
        if errors:
            logging.info(f"Found {len(errors)} issues in the pipeline.")
        else:
            logging.info("No issues found in the pipeline.")
        return errors