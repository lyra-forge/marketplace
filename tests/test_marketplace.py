import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CLAUDE = ROOT / ".claude-plugin" / "marketplace.json"
CODEX = ROOT / ".agents" / "plugins" / "marketplace.json"
README = ROOT / "README.md"


class MarketplaceParityTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.claude = json.loads(CLAUDE.read_text(encoding="utf-8"))
        cls.codex = json.loads(CODEX.read_text(encoding="utf-8"))
        cls.readme = README.read_text(encoding="utf-8")

    def test_catalogs_expose_the_same_plugins(self):
        claude_names = [entry["name"] for entry in self.claude["plugins"]]
        codex_names = [entry["name"] for entry in self.codex["plugins"]]
        self.assertEqual(codex_names, claude_names)

    def test_codex_entries_have_install_policy_and_https_sources(self):
        for entry in self.codex["plugins"]:
            with self.subTest(plugin=entry["name"]):
                self.assertEqual(entry["source"]["source"], "url")
                self.assertTrue(entry["source"]["url"].startswith("https://"))
                self.assertIn(entry["policy"]["installation"], {
                    "AVAILABLE",
                    "INSTALLED_BY_DEFAULT",
                    "NOT_AVAILABLE",
                })
                self.assertIn(entry["policy"]["authentication"], {
                    "ON_INSTALL",
                    "ON_USE",
                })
                self.assertTrue(entry["category"])

    def test_catalog_sources_use_the_same_https_repository(self):
        claude_by_name = {entry["name"]: entry for entry in self.claude["plugins"]}
        for entry in self.codex["plugins"]:
            with self.subTest(plugin=entry["name"]):
                claude_source = claude_by_name[entry["name"]]["source"]
                self.assertEqual(entry["source"]["url"], claude_source["url"])
                self.assertEqual(entry["source"].get("sha"), claude_source.get("sha"))

    def test_marketplace_does_not_duplicate_manifest_versions(self):
        for catalog in (self.claude, self.codex):
            for entry in catalog["plugins"]:
                with self.subTest(catalog=catalog["name"], plugin=entry["name"]):
                    self.assertNotIn("version", entry)

    def test_readme_has_both_install_commands_for_every_plugin(self):
        for entry in self.claude["plugins"]:
            name = entry["name"]
            with self.subTest(plugin=name):
                self.assertIn(f"/plugin install {name}@lyra-forge", self.readme)
                self.assertIn(f"codex plugin add {name}@lyra-forge", self.readme)

    def test_readme_documents_both_update_flows(self):
        self.assertIn("/plugin marketplace update lyra-forge", self.readme)
        self.assertIn("/plugin update vizier@lyra-forge", self.readme)
        self.assertIn("codex plugin marketplace upgrade lyra-forge", self.readme)


if __name__ == "__main__":
    unittest.main()
