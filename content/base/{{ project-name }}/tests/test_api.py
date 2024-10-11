from unittest import TestCase
import ai_agent.api.api as api


class Test(TestCase):
    def test_execute(self):
        api.execute()
        print("It works!")