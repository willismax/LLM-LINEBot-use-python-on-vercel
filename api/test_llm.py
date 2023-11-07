import unittest
from unittest.mock import patch, Mock
from llm import ChatGPT

class TestChatGPT(unittest.TestCase):
    """
    This class contains unit tests for the ChatGPT class.
    """
    def setUp(self):
        self.chatbot = ChatGPT()

    @patch("llm.client.chat.completions.create")
    def test_get_response(self, mock_create):
        mock_response = Mock()
        mock_response.choices[0].message.content = "Hello, how are you?"
        mock_create.return_value = mock_response

        response = self.chatbot.get_response()

        self.assertEqual(response, "Hello, how are you?")

    def test_add_msg(self):
        self.chatbot.add_msg("Hello, how are you?")
        self.assertEqual(len(self.chatbot.prompt.msg_list), 2)
        self.assertEqual(self.chatbot.prompt.msg_list[-1]["content"], "Hello, how are you?")

if __name__ == '__main__':
    unittest.main()