# Pipeline Debugging and AI Log Summarization

This project provides tools for debugging pipelines and summarizing logs using AI. It includes:
- **Pipeline Debugger**: Identifies errors and bottlenecks in pipeline logs.
- **AI Log Summarizer**: Uses OpenAI's GPT model to summarize logs.

## Prerequisites

- Python 3.14 or higher
- Virtual environment (recommended)
- OpenAI API key (for AI log summarization)

## Setup

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd ailogs
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Add your OpenAI API key:
   - Set the `OPENAI_API_KEY` environment variable:
     ```bash
     export OPENAI_API_KEY="your-api-key"
     ```

## Running the Code

### 1. Run Unit Tests
To ensure everything is working correctly:
```bash
python -m unittest discover -s tests
```

### 2. Debug Pipeline Logs
Use the `PipelineDebugger` to load and parse logs:
```python
from src.pipeline_debugger import PipelineDebugger

debugger = PipelineDebugger("./logs")
errors = debugger.debug_pipeline()
print(errors)
```

### 3. Summarize Logs with AI
Use the `AILogSummarizer` to summarize logs:
```python
from src.ai_log_summarizer import AILogSummarizer

summarizer = AILogSummarizer("your-api-key")
logs = ["ERROR: Something went wrong"]
summaries = summarizer.summarize_logs(logs)
print(summaries)
```

## Logs Directory
Ensure the `./logs` directory exists and contains log files for the `PipelineDebugger` to process.

## License
This project is licensed under the MIT License.