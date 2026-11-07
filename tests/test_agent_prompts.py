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

    def test_specialists_publish_instead_of_only_returning_final_text(self):
        for name in SPECIALISTS:
            with self.subTest(agent=name):
                text = " ".join(prompt(name).split())
                self.assertIn('switch_send_targeted_message with target_names ["studiomate-studio_manager"]', text)
                self.assertIn("Do not stop with only final text", text)
                self.assertIn("do not duplicate it in body", text)
                self.assertIn("Respond only when Studio Manager tags you", text)

    def test_manager_publishes_summary_and_does_not_delegate_verification(self):
        text = " ".join(prompt("studio_manager").split())
        self.assertIn("Use switch_post_message", text)
        self.assertIn("Never ask the agent to verify payment or open a screenshot", text)
        self.assertIn("unverified payment never block the sequence", text)

    def test_new_trials_require_published_current_deliverables(self):
        text = " ".join(prompt("studio_manager").split())
        self.assertIn("Count only published deliverables for that trial ID", text)
        self.assertIn("Do not mark Accounts Desk complete without its actual ledger", text)
        self.assertIn("never Accounts Desk", text)

    def test_order_card_preserves_source_contact_fields(self):
        text = " ".join(prompt("studio_manager").split())
        self.assertIn("customer email, phone and Telegram exactly as given", text)
        self.assertIn("Mirror the source fields", text)
        self.assertNotIn("quoted price (missing unless", text)

    def test_customer_acknowledgement_asks_lyric_feel_not_team(self):
        text = " ".join(prompt("customer_liaison").split())
        self.assertIn("lyric feel", text)
        self.assertIn("is the heart of your story", text)
        self.assertIn("internal team, artist assignments", text)


if __name__ == "__main__":
    unittest.main()
