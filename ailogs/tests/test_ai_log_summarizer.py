import unittest
from src.ai_log_summarizer import AILogSummarizer

class TestAILogSummarizer(unittest.TestCase):
    def setUp(self):
        self.summarizer = AILogSummarizer("fake-api-key")

    def test_summarize_logs(self):
        logs = ["ERROR: Something went wrong"]
        summaries = self.summarizer.summarize_logs(logs)
        self.assertEqual(len(summaries), 1, "Should return one summary.")

if __name__ == "__main__":
    unittest.main()