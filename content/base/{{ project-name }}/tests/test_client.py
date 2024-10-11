from unittest import TestCase
import ai_agent.client.client as client


class Test(TestCase):
    def test_execute(self):
        client.execute()
        print("It works!")