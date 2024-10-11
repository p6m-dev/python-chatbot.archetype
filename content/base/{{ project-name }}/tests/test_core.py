from unittest import TestCase
import ai_agent.core.core as core


class Test(TestCase):
    def test_execute(self):
        core.execute()
        print("It works!")