import unittest
from src.pipeline_debugger import PipelineDebugger

class TestPipelineDebugger(unittest.TestCase):
    def setUp(self):
        self.debugger = PipelineDebugger("./logs")

    def test_load_logs(self):
        self.debugger.load_logs()
        self.assertGreater(len(self.debugger.logs), 0, "Logs should be loaded.")

    def test_parse_logs(self):
        self.debugger.logs = ["INFO: All good", "ERROR: Something went wrong"]
        errors = self.debugger.parse_logs()
        self.assertEqual(len(errors), 1, "Should find one error in logs.")

if __name__ == "__main__":
    unittest.main()