from flask import Flask, request, jsonify
from loguru import logger
import re

app = Flask(__name__)

# Predefined log patterns and fixes
log_patterns = {
    r"timeout": "Increase timeout settings in the configuration.",
    r"connection refused": "Check if the service is running and accessible.",
    r"out of memory": "Increase memory allocation or optimize the application."
}

@app.route('/analyze', methods=['POST'])
def analyze_logs():
    data = request.get_json()
    logs = data.get('logs', [])
    
    suggestions = []
    for log in logs:
        for pattern, fix in log_patterns.items():
            if re.search(pattern, log, re.IGNORECASE):
                suggestions.append({"log": log, "suggestion": fix})
                logger.info(f"Pattern matched: {pattern} -> Suggestion: {fix}")

    return jsonify(suggestions)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)