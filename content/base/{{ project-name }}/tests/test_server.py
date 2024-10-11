from unittest import TestCase
import ai_agent.server.server as server


class Test(TestCase):
    def test_execute(self):
        server.execute()
        print("It works!")