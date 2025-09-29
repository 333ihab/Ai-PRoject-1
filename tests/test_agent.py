import unittest
from src.environment import Environment
from src.agent import BaselineAgent

class TestAgent(unittest.TestCase):
    def test_cleaning(self):
        env = Environment(2, dirt_prob=1.0)
        agent = BaselineAgent(env)
        agent.act()
        self.assertTrue(all(not r.is_dirty() for r in env.rooms))

if __name__ == "__main__":
    unittest.main()
