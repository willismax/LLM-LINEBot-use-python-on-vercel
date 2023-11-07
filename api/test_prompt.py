import unittest
from prompt import Prompt

class TestPrompt(unittest.TestCase):
    """
    This class tests the functionality of the Prompt class.
    """
    def setUp(self):
        self.prompt = Prompt()

    def test_add_msg(self):
        self.prompt.add_msg("Hello, how are you?")
        self.assertEqual(len(self.prompt.msg_list), 2)
        self.assertEqual(self.prompt.msg_list[-1]["content"], "Hello, how are you?")

    def test_generate_prompt(self):
        prompt = self.prompt.generate_prompt()
        self.assertEqual(len(prompt), 1)
        self.assertEqual(prompt[0]["role"], "system")
        self.assertIn("Welcome to our chatbot", prompt[0]["content"])

if __name__ == '__main__':
    unittest.main()