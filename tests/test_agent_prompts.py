from pathlib import Path
import unittest

RUNTIME = Path(__file__).resolve().parent.parent / "agents" / "runtime"
SPECIALISTS = ["accounts_desk", "project_manager", "creative_director", "customer_liaison"]


def prompt(name):
    return (RUNTIME / f"studiomate-{name}" / "AGENTS.md").read_text()


class AgentPromptTests(unittest.TestCase):
    def test_studio_manager_posts_native_room_mention_not_hosted_url(self):
        text = prompt("studio_manager")
        self.assertIn("Order room: ~<room-name>", text)
        self.assertIn("Never post a URL for a room", text)
        self.assertNotIn("Post the real room", text)

    def test_studio_manager_forbids_tool_syntax(self):
        text = prompt("studio_manager")
        self.assertIn("Never post tool-call syntax, XML tags, JSON", text)
        self.assertIn("Finish all tool calls before writing a message", text)

    def test_specialists_hand_back_only_to_studio_manager(self):
        for name in SPECIALISTS:
            with self.subTest(agent=name):
                text = prompt(name)
                self.assertIn("@studiomate-studio_manager", text)
                self.assertRegex(text, r"(?i)never tool-call syntax|never post tool-call syntax")

    def test_customer_acknowledgement_asks_lyric_feel_not_team(self):
        text = " ".join(prompt("customer_liaison").split())
        self.assertIn("lyric feel", text)
        self.assertIn("is the heart of your story", text)
        self.assertIn("internal team, artist assignments", text)


if __name__ == "__main__":
    unittest.main()
