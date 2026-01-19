import openai


class AILogSummarizer:
    def __init__(self, api_key):
        openai.api_key = api_key

    def summarize_logs(self, logs):
        """Summarize logs using OpenAI's GPT model."""
        summaries = []
        for log in logs:
            try:
                response = openai.Completion.create(
                    engine="text-davinci-003",
                    prompt=f"Summarize the following log:\n{log}",
                    max_tokens=100,
                )
                summaries.append(response.choices[0].text.strip())
            except Exception as e:
                summaries.append(f"Error summarizing log: {e}")
        return summaries