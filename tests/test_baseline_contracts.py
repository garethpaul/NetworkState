import importlib.util
from pathlib import Path
import subprocess
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "networkstate_check_baseline", ROOT / "scripts/check-baseline.py"
)
CHECK_BASELINE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(CHECK_BASELINE)


class GitignoreContractTests(unittest.TestCase):
    def test_comments_and_leading_whitespace_do_not_create_required_patterns(self):
        source = "# .explore/\n .explore/\n.explore-cache/\n\nDerivedData/\n"

        self.assertEqual(
            CHECK_BASELINE.active_gitignore_patterns(source),
            {" .explore/", ".explore-cache/", "DerivedData/"},
        )

    def test_later_negation_disables_effective_ignore(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            subprocess.run(["/usr/bin/git", "init", "-q"], cwd=root, check=True)
            (root / ".gitignore").write_text(".explore/\n", encoding="utf-8")
            (root / ".explore").mkdir()
            (root / ".explore/REPO_MAP.md").touch()

            self.assertTrue(CHECK_BASELINE.git_ignores(root, ".explore/"))
            self.assertTrue(
                CHECK_BASELINE.git_ignores(root, ".explore/REPO_MAP.md")
            )
            with (root / ".gitignore").open("a", encoding="utf-8") as gitignore:
                gitignore.write("!.explore/\n")
            self.assertFalse(CHECK_BASELINE.git_ignores(root, ".explore/"))
            self.assertFalse(
                CHECK_BASELINE.git_ignores(root, ".explore/REPO_MAP.md")
            )

    def test_force_added_explore_files_are_tracked(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            subprocess.run(["/usr/bin/git", "init", "-q"], cwd=root, check=True)
            (root / ".gitignore").write_text(".explore/\n", encoding="utf-8")
            (root / ".explore").mkdir()
            (root / ".explore/REPO_MAP.md").touch()
            subprocess.run(
                ["/usr/bin/git", "add", "-f", ".explore/REPO_MAP.md"],
                cwd=root,
                check=True,
            )

            self.assertEqual(
                CHECK_BASELINE.git_tracked_paths(root, ".explore"),
                [".explore/REPO_MAP.md"],
            )


class ReachabilitySnapshotContractTests(unittest.TestCase):
    def setUp(self):
        self.swift = (ROOT / "NetworkState/NetworkState.swift").read_text(encoding="utf-8")
        self.tests = (ROOT / "NetworkStateTests/NetworkStateTests.swift").read_text(encoding="utf-8")

    def test_current_snapshot_contract_is_complete(self):
        self.assertEqual(
            [],
            CHECK_BASELINE.reachability_snapshot_contract_errors(self.swift, self.tests),
        )

    def test_nil_snapshot_guard_is_required(self):
        mutated = self.swift.replace("guard let flags = flagsProvider() else", "if let flags = flagsProvider()")
        self.assertTrue(CHECK_BASELINE.reachability_snapshot_contract_errors(mutated, self.tests))

    def test_shared_flag_evaluator_is_required(self):
        mutated = self.swift.replace("return isReachableWithFlags(flags)", "return true", 1)
        self.assertTrue(CHECK_BASELINE.reachability_snapshot_contract_errors(mutated, self.tests))

    def test_tautological_live_network_assertion_is_rejected(self):
        mutated_tests = self.tests + "\n// result || !result\n"
        self.assertIn(
            "tests must not use a tautological Boolean connectivity assertion",
            CHECK_BASELINE.reachability_snapshot_contract_errors(self.swift, mutated_tests),
        )


if __name__ == "__main__":
    unittest.main()
